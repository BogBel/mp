FROM python:3.11-slim

WORKDIR /app
COPY . /app/
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
