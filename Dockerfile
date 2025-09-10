FROM 3.12.11-alpine3.22

WORKDIR /application

RUN apt-get update
RUN pip install --upgrade pip wheel "poetry==1.8.2"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install
COPY app/. .

CMD ["python", "main.py"]