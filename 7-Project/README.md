## Final Project 
- [Problem Explanation](#problem-explanation)
- [Enviroment](#enviroment)
  - [Create a conda enviroment for the project with python=3.9](#create-a-conda-enviroment-for-the-project-with-python39)
  - [Active the enviroment](#active-the-enviroment)
  - [Install the dependencies](#install-the-dependencies)
- [Model: Classification model that predict if an employee is leaving the company.](#model-classification-model-that-predict-if-an-employee-is-leaving-the-company)
  - [Dataset: IBM HR Analytics Employee Attrition & Performance](#dataset-ibm-hr-analytics-employee-attrition--performance)
  - [Download dataset with the following command:](#download-dataset-with-the-following-command)
  - [Working on model.ipynb](#working-on-modelipynb)
    - [Install ipython kernel](#install-ipython-kernel)
- [Tracking Experiment with Mlflow](#tracking-experiment-with-mlflow)
  - [Model Register](#model-register)
- [Orchestration of the project](#orchestration-of-the-project)
  - [Install prefect](#install-prefect)
  - [Authenticating with Prefect Cloud (Optional)](#authenticating-with-prefect-cloud-optional)
  - [Start orion UI](#start-orion-ui)
- [Deployment](#deployment)
  - [Build the deployment](#build-the-deployment)
  - [Apply the deployment](#apply-the-deployment)
  - [Work queues and agents](#work-queues-and-agents)
  - [Create a Workflow in the UI](#create-a-workflow-in-the-ui)
  - [Start an agent](#start-an-agent)
  - [Schedule the deployment](#schedule-the-deployment)
- [Monitoring](#monitoring)
  - [Install evidently](#install-evidently)

# Problem Explanation


# Enviroment
## Create a conda enviroment for the project with python=3.9
```
conda create -n project_enviroment python=3.9
```
## Active the enviroment
```
conda activate project_enviroment
```
## Install the dependencies
```
pip install -r requirements.txt
```
# Model: Classification model that predict if an employee is leaving the company.
## Dataset: IBM HR Analytics Employee Attrition & Performance
Download dataset [here](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
## Download dataset with the following command:
```
wget https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset?resource=download
```
## Working on [model.ipynb](notebooks/model.ipynb)
### Install ipython kernel
```
conda install -n project_enviroment ipykernel --update-deps --force-reinstall
```

# Tracking Experiment with Mlflow

Run the following command in your terminal to track the experiment in your local machine:

```
mlflow ui --backend-store-uri sqlite:///mydb.sqlite
```
That command create a database file called mydb.sqlite in the current directory that'll be used to store the experiment data.

Add this code to your notebook to track the experiment in your local machine using a SQLite database:

```
import mlflow 


mlflow.set_tracking_uri('sqlite:///mydb.sqlite')
```

And start a run with:
  
```
mlflow.start_run()
```
## Model Register
I'm using a sklearn library, mlflow provides a way to register the model with the following command:
``` 
  #Model Register
  mlflow.sklearn.log_model(
        sk_model = logreg,
        artifact_path='models/logreg',
        registered_model_name='sk-learn-logreg-model'
  )
```
![Registered model](images/mlflow-registered-model.PNG)
# Orchestration of the project
I'm going to use [Prefect](https://prefect.io/) to orchestrate the project.
## Install prefect
```
conda install prefect -c conda-forge
```
## Authenticating with Prefect Cloud (Optional)
```
prefect auth login --key <YOUR-KEY>
```
## Start orion UI
```
prefect orion start
```

# Deployment 
See the options wit the following command:

```
 prefect deployment build --help
```
## Build the deployment
```
prefect deployment build .\model.py:applying_model --name Project-Deployment --tag MLOps
```
## Apply the deployment
```
prefect deployment apply applying_model-deployment.yaml
```
## Work queues and agents
We can't run the deployment from the UI yet. We nned a work queue and an agent to run the deployment.

Work queues and agents are the mechanisms by which the Prefect API orchestrates deployment flow runs in remote execution environments.

Work queues let you organize flow runs into queues for execution. Agents pick up work from queues and execute the flows
## Create a Workflow in the UI
![Work Queue](images/prefect-work-queue.PNG)
## Start an agent
```
prefect agent start -t tag where tag is the tag you used to build the deployment.
```
Now, when you run a deployment with the `-t tag` option, the agent will pick up the work from the queue and execute the flows.
## Schedule the deployment
- Go to the UI
- Select `Add Schedule`
![Schedule](images/prefect-schedule.png)
- I'm going to select `Cron` with a value of `0 0 * * *` that means every day at 12:00 AM.
- `Timezone` is important, so, be sure to select the correct timezone.

# Monitoring
I'm going to use [Evidently](https://evidentlyai.com/) to monitor the experiment.

## Install evidently
You can install it with the following command:
```
pip install evidently
```
