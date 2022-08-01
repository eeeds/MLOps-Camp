import pandas as pd
from datetime import datetime
import os 
from batch import main, get_input_path, get_output_path

S3_ENDPOINT_URL = 'http://localhost:4566'

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)

def prepare_data(df, categorical):

    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def output_file():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    df_prepared = prepare_data(df, ['PUlocationID', 'DOlocationID'])

    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    
    df_prepared.to_parquet(
            's3://nyc-duration/test/test.parquet',
            engine='pyarrow',
            compression=None,
            index=False,
            storage_options=options)

def test():
    main(2021,1)
    
    categorical = ['PUlocationID', 'DOlocationID']
    input_file = get_output_path(2021,1)

    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    df_output = pd.read_parquet(input_file, storage_options=options)

    sum_predictions = df_output['predicted_duration'].sum()

    assert sum_predictions == 34, f"sum: {sum_predictions}"


if __name__ == "__main__":
    output_file()

