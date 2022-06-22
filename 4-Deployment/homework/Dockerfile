FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install -U pip 
RUN pip install pipenv


COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy 

RUN pip install pandas
RUN pip install pyarrow
RUN pip install fastparquet


COPY ["starter.py", "./"]


ENTRYPOINT [ "python3", "starter.py"]