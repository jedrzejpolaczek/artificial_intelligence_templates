# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv sync --system

COPY ./src /code/

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload
