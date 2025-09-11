FROM python:3.12-bookworm

WORKDIR /application

RUN apt-get update
RUN pip install --upgrade pip wheel "poetry==1.8.2"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev
COPY project/ .

CMD ["python", "main.py"]