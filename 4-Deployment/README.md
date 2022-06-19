## Model Deployment
# 4. Model Deployment

## 4.1 Three ways of deploying a model
-   Batch Offline: You run your model regularly (hourly, daily, monthly). Pull the data from the DB and then apply the model.
-   Batch Online: It's running all the time. It's always available. You can run your models using Web Services (relationship 1 x 1 between client-server) and Streaming ( 1 x n relationship)


## 4.2 Web-services: Deploying models with Flask and Docker
### Install python, scikit learn and flask on a virtual environment with pipenv:
```
pipenv install scikit-learn==1.0.2 flask --python=3.9
```
### Go to the env with the command:
```
pipenv shell
```
## You can use anaconda to create the venv:
```
conda create -n web-service python=3.9
```
## Go to the env with the command:
```
conda activate web-service
```
### Install the dependencies:
```
pip install -r requirements.txt
```
## Work on predict.py
[See code here](web-service/)


## 4.3 Web-services: Getting the models from the model registry (MLflow)

<a href="https://www.youtube.com/watch?v=aewOpHSCkqI&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK">
  <img src="images/thumbnail-4-03.jpg">
</a>


[See code here](web-service-mlflow/)


## 4.4 (Optional) Streaming: Deploying models with Kinesis and Lambda 

<a href="https://www.youtube.com/watch?v=TCqr9HNcrsI&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK">
  <img src="images/thumbnail-4-04.jpg">
</a>


[See code here](streaming/)


## 4.5 Batch: Preparing a scoring script

<a href="https://www.youtube.com/watch?v=18Lbaaeigek&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK">
  <img src="images/thumbnail-4-05.jpg">
</a>


[See code here](batch/)


## 4.6 Batch: TBA

COMING SOON



## 4.7 Homework

COMING SOON


## Notes

Did you take notes? Add them here:

* Send a PR, add your notes above this line