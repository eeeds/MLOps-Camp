

import os
import uuid
import pickle
import sys 

from datetime import datetime 
import pandas as pd


from dateutil.relativedelta import relativedelta

import mlflow

from prefect import task, flow, get_run_logger


from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline

@flow
def ride_duration_prediction(
    taxi_type: str,
    run_id:str,
    run_date: datetime=None):

    if run_date is None:
        ctx = get_run_context()
        date = ctx.flow_run_expected_start_time

    input_file, output_file = get_paths(run_date, taxi_type, run_id)
    apply_model(
        input_file=input_file,
        run_id=run_id, 
        output_file=output_file)

def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts




def load_model(run_id):
    logged_model = f's3://mlflow-models-esteban/1/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def save_results(df, y_pred, run_id, output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id
    print(f'Saving the results to {output_file}')
    df_result.to_parquet(output_file, index=False)

def get_paths(run_date, taxi_type, run_id):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month 

    input_file = f's3://nyc-tlc/trip data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f's3://mlflow-models-esteban/taxi_type={taxi_type}/year={year:04d}/month={month:02d}/{run_id}.parquet'

    return input_file, output_file

@task
def apply_model(input_file, run_id, output_file):
    logger = get_run_logger()
    logger.info(f'Reading the data from  {input_file}')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    logger.info(f'Loading the model with RUN_iD={run_id}')
    model = load_model(run_id)
    logger.info(f'Applying the model')
    y_pred = model.predict(dicts)
    logger.info(f'Saving the results to {output_file}')
    save_results(df, y_pred, run_id, output_file)

    return output_file
def run():
    taxi_type = sys.argv[1] #green
    year = int(sys.argv[2]) #2021
    month = int(sys.argv[3]) # 3
    RUN_ID = sys.argv[4] # '133f7f2c17384132b4d4f76682ab6139'
    

    #RUN_ID = os.getenv('RUN_ID', 'e1efc53e9bd149078b0c12aeaa6365df')

    ride_duration_prediction(
        taxi_type=taxi_type,
        run_id=RUN_ID,
        run_date=datetime(year, month, 1))


if __name__ =='__main__':
    run()





