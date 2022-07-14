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
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v2
```
Then, work on the `model_test.py` file again.
## 6.2 Integration tests with docker-compose



## 6.3 Testing cloud services with LocalStack



## 6.4 Code quality: linting and formatting




## 6.5 Git pre-commit hooks




## 6.6 Makefiles and make



## 6.X Homework


More information here: [homework.md](homework.md)
