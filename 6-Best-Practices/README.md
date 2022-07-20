# 6. Best Practices

## 6.1 Testing Python code with pytest
Copy all the files from the folder `4-Deployment/streaming` to the folder `code` in the `Best Practices` folder.
```
cp -r 4-Deployment/streaming 6-Best-Practices/code
```
Create the pipenv enviroment with:
```
pipenv install
```
In my case I'm using conda:
```
conda activate env
```
Install pytest (conda)
```
pip install pytest
```
Install pytest(Pipenv)
```
pipenv install --dev pytest
```
Select the python interpreter on VS Code that you want to use:
```
Ctrl+Shift+P->Type `Python Interpreter`->Select the python interpreter that you want to use
```
Go to the extension and select the folder `tests` for the tests.

Add a `__init__.py` file to the folder `tests` to make it a python package.

Working on `model_test.py` file.

Following the video, making changes to the `lambda_function.py` file and `model.py` file.

Build the docker image with:
```
docker build -t stream-model-duration:v2 .
```
Test it with:
```
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="133f7f2c17384132b4d4f76682ab6139" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v2
```
Then, work on the `model_test.py` file again.
## 6.2 Integration tests with docker-compose

-   Following the video
-   Using `Deepdiff` to compare the results of the model with the results of the test.
-   Install it with `pip install deepdiff`
-   Working on `model_test.py` file and `test_docker.py` files.
-   Build the docker image with:
    ```
    docker build -t stream-model-duration:v2 .
    ``` (because we have installed deepdiff)

- Re run the test with:
    ```
    docker run -it --rm \
        -p 8080:8080 \
        -e PREDICTIONS_STREAM_NAME="ride_predictions" \
        -e RUN_ID="133f7f2c17384132b4d4f76682ab6139" \
        -e TEST_RUN="True" \
        -e AWS_DEFAULT_REGION="eu-west-1" \
        stream-model-duration:v2
    ```
-   Compare the results of the model with the results of the test running `test_docker.py` file.
-   Create [integration-test folder](code/integration-test) and move the `test_docker.py` file to it.
-   Download the model from ` aws s3 ls s3://mlflow-models-esteban/1/133f7f2c17384132b4d4f76682ab6139/artifacts/model ` with the following command:
    ```
    aws s3 cp --recursive s3://mlflow-models-esteban/1/133f7f2c17384132b4d4f76682ab6139/artifacts/model model
    ```
-   Crete `run.sh` file 
-   Create `docker-compose.yml` file and move it to the `integration-test` folder.
-   Run `docker build -t ${LOCAL_IMAGE_NAME} ..` to build the docker image.
-   Run `docker-compose up -d` to start the docker-compose.

## 6.3 Testing cloud services with LocalStack



## 6.4 Code quality: linting and formatting




## 6.5 Git pre-commit hooks




## 6.6 Makefiles and make



## 6.X Homework


More information here: [homework.md](homework.md)

