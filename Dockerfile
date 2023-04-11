FROM python:3.10-slim

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy the scripts to the folder
COPY ./task_app /app/task_app

# start the server
CMD ["uvicorn", "task_app.main:app", "--host", "0.0.0.0", "--port", "80"]