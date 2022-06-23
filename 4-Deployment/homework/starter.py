#!/usr/bin/env python
# coding: utf-8


import pickle
import pandas as pd
import sys 


with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)

categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def run():
    ## Create parameters for the model
    year = int(sys.argv[1])
    month = int(sys.argv[2])

    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year}-0{month}.parquet')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    #Print the y_pred mean
    print('Y_pred value is: ',y_pred.mean())
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    # write the ride id and the predictions to a dataframe with results
    df_result = pd.DataFrame({'ride_id': df.ride_id, 'prediction': y_pred})

    # Saving the results of the model into a parquet file.
    df_result.to_parquet(
        'output_file',
        engine='pyarrow',
        compression=None,
        index=False
    )


if __name__ == '__main__':
    run()


