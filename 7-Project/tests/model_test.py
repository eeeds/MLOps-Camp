import pandas as pd


def extract_data():
    """
    Extract data from csv file and return dataframe

    Returns:
        pd.DataFrame: dataframe with data

    """
    df = pd.read_csv('./datasets/HR-Employee-Attrition.csv')
    # Delete unnecessary columns
    df.drop(['EmployeeCount', 'EmployeeNumber', 'StandardHours'], axis=1, inplace=True)
    # Changing categorical data to numerical data
    df['Attrition'] = df['Attrition'].apply(lambda x: 1 if x=='Yes' else 0)
    df['Over18'] = df['Over18'].apply(lambda x: 1 if x=='Yes' else 0)
    df['OverTime'] = df['OverTime'].apply(lambda x: 1 if x=='Yes' else 0)

    assert df.shape ==(1470,32)


