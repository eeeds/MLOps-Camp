## Second Week of the Zoomcamp
## Import Concepts
* ML Experiment: the process of building an ML model.
* Experiment run: each trial in an ML experiment.
* Run artifact: any file that is associated with an ML run.
* Experiment metadata : Result of all the runs of an experiment.

## Why is experiment tracking important?
* Reproducibility: if you run the same experiment multiple times, you will get the same results.
* Organization : You can organize your experiments in folders and subfolders.
* Optimization: You can run the same experiment multiple times with different hyperparameters.

## Tracking experiments in spreadsheets
## Why is not enough?
* Error prone
* No standard format
* Visibility and Collaboration
## MLflow
An open source plattform for the machine learning research.
It's just a python library that allows you to track your experiments and it contains:
* Tracking
* Models
* Model Registry
* Projects

![Tracking Experiments with MLflow](tracking_experiments.PNG)

## I'll use conda for create a environment for my experiments with Python = 3.9
```
conda create -n mlflow_enviroment python=3.9
```
## Activate enviroment
```
activate mlflow_enviroment
```

## Install Mlflow with this command
```
pip install mlflow
```

## Install all the libraries that we gonna use
```
pip install -r requirements.txt
```
## Run MLflow UI with backend configure (Remember to put this command in path of the files that you want to track)
```
mlflow ui --backend-store-uri=sqlite:///mlflow.db
```

