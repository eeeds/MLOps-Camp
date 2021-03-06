# 5. Model Monitoring



## 5.1 Monitoring for ML-based services
1. Add ML metrics to service health monitoring (Prometheus/Grafana)
2. Build an ML focused Dashboard(s) (MongoDB/Grafana or BI tools Tableu, Looker)

![Monitoring](images/monitoring.PNG)

-   You can add batch monitoring to this system

### Working on prediction_service folder
1. Install all the libraries with `pip install -r requirements.txt`
2. Setting constants for the model (MODEL_FILE, MONGODB_ADDRESS, EVIDENTLY_SERVICE_ADDRESS)
3. Working on `app.py` file
4. Run `docker-compose up --build`
5. Test the app with `test.py`
    ```
    python3 test.py
    ```
6. You should see the app running on localhost:5000

![App working](images/monitoring-working.PNG)


## 5.2 Setting up the environment
1. Create a conda enviroment:
  ```
    conda create -n mlops5 python=3.8
  ```
2. Activate the conda enviroment:
  ```
    conda activate mlops5
  ```
3. Install all the libraries with `pip install -r requirements.txt` (monitoring folder)

4. [Create prepare.py Script](prepare.py)

5. [Create Dockerfile](docker-compose.yml)
## 5.3 Creating a prediction service and simulating traffic
- Following the video
- Working on [send_data.py](send_data.py)
- Open your conda enviroment (make sure that you container is running)
- Run `python send_data.py`
- Create `pymongo_example.ipynb` to see the data in your mongo db.
- You can check it: [pymongo_example.ipynb](pymongo_example.ipynb)


## 5.4 Realtime monitoring walktrough (Prometheus, Evidently, Grafana)
- Following the video
- Working on [monitoring/evidently_service](evidently_service)


## 5.5 Batch monitoring walktrough (Prefect, MongoDB, Evidently)
- Following the video
- Working on [prefect_example.py](prefect_example.py)
- Open your conda enviroment (make sure that you container is running)
- Run `python prefect_example.py`
- Run `prefect orion start` to see the the task in the Orion UI
- See the data with the jupyter notebook that we were created before, [pymongo_example.ipynb](pymongo_example.ipynb)
- See the html report that evidently had created.


## 5.6 Homework

No HW for this week.



# Monitoring example

## Prerequisites

You need following tools installed:
- `docker`
- `docker-compose` (included to Docker Desktop for Mac and Docker Desktop for Windows )

## Preparation

Note: all actions expected to be executed in repo folder.

- Create virtual environment and activate it (eg. `python -m venv venv && ./venv/bin/activate`)
- Install required packages `pip install -r requirements.txt`
- Run `python prepare.py` for downloading datasets

## Monitoring Example

### Starting services

To start all required services, execute:
```bash
docker compose up
```

It will start following services:
- `prometheus` - TSDB for metrics
- `grafana` - Visual tool for metrics
- `mongo` - MongoDB, for storing raw data, predictions, targets and profile reports
- `evidently_service` - Evindently RT-monitoring service (draft example)
- `prediction_service` - main service, which makes predictions

### Sending data

To start sending data to service, execute:
```bash
python send_data.py
```

This script will send every second single row from dataset to prediction service along with creating file `target.csv` with actual results (so it can be loaded after)

## Batch Monitoring Example

After you stop sending data to service, you can run batch monitoring pipeline (using Prefect) by running script:

```bash
python prefect_example.py
```

This script will:
- load `target.csv` to MongoDB
- download dataset from MongoDB
- Run Evidently Model Profile and Evidently Report on this data
- Save Profile data back to MongoDB
- Save Report to `evidently_report_example.html`

You can look at Prefect steps in Prefect Orion UI
(to start it execute `prefect orion start`)