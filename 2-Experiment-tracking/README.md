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

## Hyperparameter Optimizaiton Tracking:

By wrapping the `hyperopt` Optimization objective inside a `with mlflow.start_run()` block, we can track every optimization run that was ran by `hyperopt`. We then log the parameters passed by `hyperopt` as well as the metric as follows:

```python


import xgboost as xgb

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

train = xgb.DMatrix(X_train, label=y_train)
valid = xgb.DMatrix(X_val, label=y_val)

def objective(params):
    with mlflow.start_run():
        mlflow.set_tag("model", "xgboost")
        mlflow.log_params(params)
        booster = xgb.train(
            params=params,
            dtrain=train,
            num_boost_round=1000,
            evals=[(valid, 'validation')],
            early_stopping_rounds=50
        )
        y_pred = booster.predict(valid)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

    return {'loss': rmse, 'status': STATUS_OK}

search_space = {
    'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
    'learning_rate': hp.loguniform('learning_rate', -3, 0),
    'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
    'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
    'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
    'objective': 'reg:linear',
    'seed': 42
}

best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=50,
    trials=Trials()
)

```

In this block, we defined the search space and the objective than ran the optimizer. We wrap the training and validation block inside `with mlflow.start_run()` and log the used parameters using `log_params` and validation RMSE using `log_metric`.

In the UI we can see each run of the optimizer and compare their metrics and parameters. We can also see how different parameters affect the RMSE using Parallel Coordinates Plot, Scatter Plot (1 parameter at a time) and Contour Plot.
## Filter in the UI
```
tags.model='xgboost'
```
## Autologging: 

Instead of logging the parameters by "Hand" by specifiying the logged parameters and passing them. We may use the Autologging feature in MLflow. There are two ways to use Autologging; First by enabling it globally in the code/Notebook using 
```python
mlflow.autolog()
```

or by enabling the framework-specific autologger; ex with XGBoost:

```python
mlflow.xgboost.autolog()
```
Both must be done before running the experiments.

The autologger then not only stores the model parameters for ease of use, it also stores other files inside the `model` (can be specified) folder inside our experiment artifact folder, these files include:
+ `conda.yaml` and `requirements.txt`: Files which define the current envrionment for use with either `conda` or `pip` respectively
+ `MLmodel` an internal MLflow file for organization
+ Other framework-specific files such as the model itself
## Loading Models:

We can use the model to make predictions with multiple ways depending on what we need:
+ We may load the model as a Spark UDF (User Defined Function) for use with Spark Dataframes
+ We may load the model as a MLflow PyFuncModel structure, to then use to predict data in a Pandas DataFrame, NumPy Array or SciPy Sparse Array. The obtained interface is general for all models from all frameworks
+ We may load the model as is, i.e: load the XGBoost model as an XGBoost model and treat it as such

The first two methods are explained briefly in the MLflow artifacts page for each run, for the latter we may use (XGBoost example):
```python
logged_model = 'runs:/9245396b47c94513bbf9a119b100aa47/models' # Model UUID from the MLflow Artifact page for the run

xgboost_model = mlflow.xgboost.load_model(logged_model)
```
the resultant `xgboost_model` is an XGBoost `Booster` object which behaves like any XGBoost model. We can predict as normal and even use XGBoost Booster functions such as `get_fscore` for feature importance.
