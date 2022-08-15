# Import libraries
import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


from prefect import task, flow

import mlflow

mlflow.set_tracking_uri("sqlite:///mydb.sqlite")
EXPERIMENT_NAME = "hr-employee-attrition-project"

mlflow.set_experiment(EXPERIMENT_NAME)
@task(name = 'Create Pipeline', retries = 3)
def create_pipeline(train_dicts, y_train):
    """
    Create a pipeline to train a model.

    Args:
        train_dicts : list of dicts
            The list of dictionaries to use for training.
        y_train : list of floats    
            The list of target values to use for training.

    Returns:
        sklearn.pipeline.Pipeline:The pipeline to use for training.

    """
    pipeline = make_pipeline(
        DictVectorizer(),
        MaxAbsScaler(),
        LogisticRegression(),
    )
    pipeline.fit(train_dicts, y_train)
    #Save the pipeline to a file
    with open('models/pipeline.bin', 'wb') as f:
        pickle.dump(pipeline, f)

@task(name = 'Extract_Data', retries = 3)
def extract_data() -> pd.DataFrame:
    """
    Extract data from csv file and return dataframe

    Returns:
        pd.DataFrame: dataframe with data

    """
    df = pd.read_csv('datasets/HR-Employee-Attrition.csv')
    # Delete unnecessary columns
    df.drop(['EmployeeCount', 'EmployeeNumber', 'StandardHours'], axis=1, inplace=True)
    # Changing categorical data to numerical data
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})
    df['Over18'] = df['Over18'].map({'Yes':1, 'No':0})
    df['OverTime'] = df['OverTime'].map({'Yes':1, 'No':0})

    return df

@task(name ='Transform_data' ,retries = 3)
def transform_data(df: pd.DataFrame):
    """
    Transform dataframe to get features and labels

    Args:
        df (pd.DataFrame): dataframe with data
    Returns:
        X_train (csr_matrix): features for training
        y_train (array): labels for training
        X_val (csr_matrix): features for validation
        y_val (array): labels for validation
    """
    #Categorical data 
    categorical = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']
    #Numerical data
    numerical = ['Age', 'DailyRate', 'DistanceFromHome',	'Education', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',	'JobLevel',	'JobSatisfaction',	'MonthlyIncome',	'MonthlyRate',	'NumCompaniesWorked',	'OverTime',	'PercentSalaryHike', 'PerformanceRating',	'RelationshipSatisfaction',	'StockOptionLevel',	'TotalWorkingYears'	,'TrainingTimesLastYear'	, 'WorkLifeBalance',	'YearsAtCompany'	,'YearsInCurrentRole', 'YearsSinceLastPromotion',	'YearsWithCurrManager']
        
    ## Divide the data into train and test
    df_train_all, df_test =train_test_split(df, test_size = 0.25, random_state = 0)
    
    ##Obtain y values
    y_train_all = df_train_all['Attrition'].astype(int).values
    y_test = df_test['Attrition'].astype(int).values

    ## Training model 
    df_train, df_val = train_test_split(df_train_all, test_size = 0.25, random_state = 0)
    y_train = df_train['Attrition'].astype(int).values
    y_val = df_val['Attrition'].astype(int).values
    
    ## Use DictVectorizer()
    train_dicts = df_train[categorical + numerical].to_dict(orient = 'records')
    val_dicts = df_val[categorical + numerical].to_dict(orient = 'records')
    
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    X_val = dv.transform(val_dicts)
    
    ## Applying MaxAbsScaler() to the data
    scaler = MaxAbsScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    return X_train, y_train, X_val, y_val, train_dicts

@flow(name = 'Applying ML Model')
def applying_model():
    """
    Apply model to data

    Returns:
        None
    
    """
    df = extract_data()
    X_train, y_train, X_val, y_val, train_dicts = transform_data(df)
    with mlflow.start_run():
        # Create tags and log params
        mlflow.set_tag('model_type', 'logistic_regression')
        mlflow.set_tag('developer', 'Esteban')
        mlflow.log_param('train-data-path', 'datasets/employee_data.csv')
        mlflow.log_param('val-data-path', 'datasets/employee_data.csv')
        # Create Model
        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)
        y_pred = logreg.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        mlflow.log_metric('accuracy', accuracy)

        mlflow.log_artifact(local_path='models/logreg.pkl',
                            artifact_path='models/logreg')
        #Model Register
        mlflow.sklearn.log_model(
            sk_model = logreg,
            artifact_path='models/logreg',
            registered_model_name='sk-learn-logreg-model'
        )
    #Call create_pipeline()
    create_pipeline(train_dicts, y_train)
    return logreg


if __name__ == '__main__':
    """
    This is the main function that will be executed when you run this file
    """
    logreg = applying_model()
    # Save model to pickle file
    with open('models/logreg.pkl', 'wb') as f:
        pickle.dump(logreg, f)
    print('Model has been trained and saved')
