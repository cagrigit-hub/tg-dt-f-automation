FROM python:3.10.1

ENV PYTHONUNBUFFERED True


ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt


CMD exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT --timeout 600 --threads 8
