FROM python:3.8

WORKDIR /bionir_pipeline-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./bionir_pipeline ./bionir_pipeline
COPY ./examples ./examples

CMD [ "python", "./examples/singlePipeline/app.py"]