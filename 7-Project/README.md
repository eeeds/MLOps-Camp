
[![Code: Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)](https://code.visualstudio.com/)
[![Pandas: Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Python: Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Scklearn: Scikit Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[<img src="images/prefect-badge.png" width="200" height="42">](https://prefect.io)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=whit)](https://www.docker.com)
[<img src="images/mlflow-logo.png" width="100" height="42">](https://mlflow.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.com)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

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
  - [Evidently](#evidently)
  - [Install evidently](#install-evidently)
  - [Dashboard for classification report](#dashboard-for-classification-report)
  - [Results](#results)
  - [Whylogs](#whylogs)
  - [Install whylogs](#install-whylogs)
  - [Get your API key](#get-your-api-key)
  - [First approach: Connect dataset](#first-approach-connect-dataset)
  - [Results](#results-1)
  - [Activate Presets](#activate-presets)
- [Tests](#tests)
  - [Configure Tests](#configure-tests)
- [Linting and Formatting](#linting-and-formatting)
  - [Intall Pylint](#intall-pylint)
  - [Lint the code](#lint-the-code)
  - [Runs Results](#runs-results)
  - [View Results in Visual Studio Code](#view-results-in-visual-studio-code)
  - [Add `.pylintrc` file](#add-pylintrc-file)
  - [Formatting with black and isort](#formatting-with-black-and-isort)
  - [Add Black to pyproject.toml](#add-black-to-pyprojecttoml)
  - [Apply Isort](#apply-isort)
  - [Add Isort to pyproject.toml](#add-isort-to-pyprojecttoml)
- [Git pre-commits hooks](#git-pre-commits-hooks)
  - [Install pre-commit](#install-pre-commit)

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
![Schedule](images/prefect-schedule.PNG)
- I'm going to select `Cron` with a value of `0 0 * * *` that means every day at 12:00 AM.
- `Timezone` is important, so, be sure to select the correct timezone.

# Monitoring
I'm going to use [Evidently](https://evidentlyai.com/) and [Whylogs](https://github.com/whylabs/whylogs)to monitor the experiment.
## Evidently
## Install evidently
You can install it with the following command:
```
pip install evidently
```
## Dashboard for classification report
Classification Performance report evaluates the quality of a classification model. It works both for binary and multi-class classification. If you have a probabilistic classification, refer to a separate report.
This report can be generated for a single model, or as a comparison. You can contrast your current production model performance against the past or an alternative model.

[More info here](https://docs.evidentlyai.com/reports/classification-performance)

## Results
Using train data and valid data to evaluate the model I've created the following dashboard:
![Results](images/evidently-dashboard.PNG)
You can see the resuls in the [`dashboard`](dashboards/df_model_performance.html) folder.
## Whylogs
## Install whylogs
```
pip install "whylogs<1.0" 
```
We're installing this version because the platform doesn't yet support v1.
## Get your API key
Go to [whylogs.com](https://whylogs.com/) and create an account, then go to your profile and click on the `API` tab.
## First approach: Connect dataset
As a first approach, we can connect the dataset to the experiment.

I've used the following command to connect the dataset to the experiment:
```
import whylogs as why
from whylogs.app import Session
from whylogs.app.writers import WhyLabsWriter

writer = WhyLabsWriter("", formats=[])
    session = Session(project="model-1", pipeline="mlops-project-pipeline", writers=[writer])

with session.logger(tags={"datasetId": "model-1"}) as ylog:
        ylog.log_dataframe(df)
```
## Results
![images](images/whylogs-df.PNG)
## Activate Presets
We can activate some `Preset monitors` to monitor different part of the experiment.

You can receive alerts from these `Preset monitors`, in my case I've enabled:
![Presets](images/whylabs-presets.PNG)
# Tests 
I'll use Pytest to test the model.

Install pytest with the following command:
```
pip install pytest
```
## Configure Tests
1. Go to `tests` extension in VS Code and select a folder that contains the tests, in this case `tests/`.
2. Select `Pytest` as the test runner.

# Linting and Formatting
I'm going to use [Pylint](https://black.readthedocs.io/en/stable/) to lint and format the code.
## Intall Pylint
Use this command to install pylint:
```
pip install pylint
```
## Lint the code
You can lint your python file as follows:
```
pylint my_file.py
```
In my case, `pylint model.py`. 

## Runs Results
1. In the first time I'd obtained a score 5.23/10 (very bad).
2. Score of 5.88/10 (still bad).
3. Score of 6.47/10 (quite good).
4. After creating [pyproject.toml](pyproject.toml) my score raises to 8.35/10 (very good).
5. Now my score is 9.76/10 (excellent).
## View Results in Visual Studio Code
1. Press `Ctrl + Shift + P` and then type `linting` and select `Pylint`.
2. Run linting with `Ctrl + Shift + P` and `Run linting`.
## Add `.pylintrc` file
You can add a `.pylintrc` file in the root of the project to configure pylint.

I'm going to use `pyproject.toml` instead.
## Formatting with black and isort
Install black and isort with the following command:
```
pip install black isort
```
Before you run black, you can check the changes that will do with the following command:
```
black --diff my_file.py
```
After that, you can run black with the following command:
```
black my_file.py
```
## Add Black to pyproject.toml
You can add some configurations to `pyproject.toml`, in my case:
```
[tool.black]
line-length = 120
target-version = ['py39']
skip-string-normalization = true
```
where: 
- `line-length` is the maximum length of a line.
- `target-version` is the version of python that you want to use.
- `skip-string-normalization` is a boolean that indicates if you want to skip string normalization.
## Apply Isort
You can apply isort with the following command:
```
isort my_file.py
```
## Add Isort to pyproject.toml
Add the following configurations to `pyproject.toml`:
```
multi_line_output = 3
length_sort = true
order_by_type = true
```
where:
- `multi_line_output` is the number of lines that will be used to output a multiline string.
- `length_sort` is a boolean that indicates if you want to sort by length.
- `order_by_type` is a boolean that indicates if you want to order by type.

# Git pre-commits hooks
I'm going to install `pre-commit` library. [More info here](https://pre-commit.com/).
## Install pre-commit
```
pip install pre-commit
```