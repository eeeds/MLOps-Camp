# Import libraries
import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


from prefect import task, flow

import mlflow

mlflow.set_tracking_uri("sqlite:///mydb.sqlite")
EXPERIMENT_NAME = "hr-employee-attrition-project"

mlflow.set_experiment(EXPERIMENT_NAME)

@task(name = 'Extract_Data', retries = 3)
def extract_data() -> pd.DataFrame:
    """
    Extract data from csv file and return dataframe
    """
    employee_df = pd.read_csv('datasets/HR-Employee-Attrition.csv')
    return employee_df

@task(name ='Transform_data' ,retries = 3)
def transform_data(employee_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform dataframe to get features and labels
    """
    # Changing categorical data to numerical data
    employee_df['Attrition'] = employee_df['Attrition'].apply(
        lambda x: 1 if x == 'Yes' else 0)
    employee_df['Over18'] = employee_df['Over18'].apply(
        lambda x: 1 if x == 'Yes' else 0)
    employee_df['OverTime'] = employee_df['OverTime'].apply(
        lambda x: 1 if x == 'Yes' else 0)
    # Drop unnecessary columns
    employee_df.drop(['EmployeeCount', 'StandardHours',
                     'EmployeeNumber'], axis=1, inplace=True)
    # Categorical variables
    X_cat = employee_df[['BusinessTravel', 'Department',
                         'EducationField', 'Gender', 'JobRole', 'MaritalStatus']]
    onehot = OneHotEncoder()
    X_cat = onehot.fit_transform(X_cat).toarray()
    # Convert X_cat to df
    X_cat = pd.DataFrame(X_cat)
    # Convert X_cat to df
    X_cat = pd.DataFrame(X_cat)
    # Numerical variables
    X_numerical = employee_df[['Age', 'DailyRate', 'DistanceFromHome',	'Education', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',	'JobLevel',	'JobSatisfaction',	'MonthlyIncome',	'MonthlyRate',	'NumCompaniesWorked',	'OverTime',
                               'PercentSalaryHike', 'PerformanceRating',	'RelationshipSatisfaction',	'StockOptionLevel',	'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',	'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',	'YearsWithCurrManager']]
    # Concat X_num and X_cat
    X_all = pd.concat([X_cat, X_numerical], axis=1)
    # Scaling data
    scaler = MinMaxScaler()
    X_all = scaler.fit_transform(X_all)
    # Our target variable is Attrition
    y = employee_df['Attrition']
    return X_all, y

@flow(name = 'Applying ML Model')
def applying_model():
    """
    Apply model to data
    
    """
    employee_df = extract_data()
    X_all, y = transform_data(employee_df)
    with mlflow.start_run():
        X_train, X_test, y_train, y_test = train_test_split(
            X_all, y, test_size=0.25, random_state=0)
        # Create a tag
        mlflow.set_tag('model_type', 'logistic_regression')
        mlflow.set_tag('developer', 'Esteban')
        mlflow.log_param('train-data-path', 'data/employee_data.csv')
        mlflow.log_param('test-data-path', 'data/employee_data.csv')
        # Create Model
        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)
        y_pred = logreg.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        mlflow.log_metric('accuracy', accuracy)

        mlflow.log_artifact(local_path='models/logreg.pkl',
                            artifact_path='models/logreg')
        #Model Register
        mlflow.sklearn.log_model(
            sk_model = logreg,
            artifact_path='models/logreg',
            registered_model_name='sk-learn-logreg-model'
        )




if __name__ == '__main__':
    """
    This is the main function that will be executed when you run this file
    """
    applying_model()
    print('Model has been trained and saved')
