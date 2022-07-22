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
-   Following the video
-   Install localstack with `pip install localstack`
-   Run `docker-compose up kinesis` to start the localstack.
-   Test it with `aws --endpoint-url=http://localhost:4566 kinesis list-streams`, the result should be `[]` because we haven't created any stream.
-   Create a stream with `aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name ride_predictions --shard-count 1`

-   Obtain the shard-iterator with:
    ```aws  --endpoint-url=http://localhost:4566 \
    kinesis get-shard-iterator \
    --shard-id shardId-000000000000 \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ride_predictions \
    --query 'ShardIterator'
    ```
-   Copy the Shard Iterator and then get Results with `aws --endpoint-url=http://localhost:4566 kinesis get-records --shard-iterator AAAAAAAAAAEKI4NpH/+OBt9nuDiWveLMU3AC04xCuNo+FAd4A8AG0xie44BvI515xlgURUqDa4yQNbbebn/Mh43NjDCW6tJ8aD87X9PTooaZWjpWklDFXATaLHKT3f+lZSyrsNC8dkb7sS/uLQHyb5OrMKM8YS7kj+LqrX93tZ3hRRaiTavCLF2HYvDA5opnP8sM3/y/dciH2NWrE4PrT4YHoJXSoknd `

-   Echo the Data value as follows `echo $DATA | base64 -d`
-   Create `test_kinesis.py` file to test the stream.
## 6.4 Code quality: linting and formatting
-   Following the video
-   Install `Pylint` with `pip install pylint`
-   Test a file with `pylint filename`
-   You can test all the files in the folder with `pylint --recursive=y .`
-   Use it in VSCode with `Ctrl+Shift+P->Python: Select Linter`->`Pylint` 
-   Now you can see the errors in the code.
-   You can add the file `.pylintrc` to configure the linter.
-   We can use pyproject.toml to configure the linter (global settings).
-   Install `black` with `pip install black`
    ```
    Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters.

    Blackened code looks the same regardless of the project you're reading. Formatting becomes transparent after a while and you can focus on the content instead.

    ```
-   Install `isort` with `pip install isort`. Isort is a tool for managing Python imports. It can sort imports alphabetically, sort imports by their type, and sort imports by their scope.
-   Type `black --diff .`. This option will show you the changes that black would make to the code.
-   Type `isort --diff .`. This option will show you the changes that isort would make to the code.
-   Run  `isort .` to sort the code, then run `black .` to format the code, then `pylint --recursive=y .` to check the code and run `pytest tests/` to test the code.



## 6.5 Git pre-commit hooks
We're gonna use the `pre-commit` tool to run the linter and the tests.
-   Following the video
-   Install `pre-commit` with `pip install pre-commit`
-   Type `pre-commit sample-config` to see the sample config.
-   Type `pre-commit install` to install the hooks. It should show you the hooks that are installed:
    ```
    pre-commit installed at .git\hooks\pre-commit
    ```





## 6.6 Makefiles and make



## 6.X Homework


More information here: [homework.md](homework.md)

