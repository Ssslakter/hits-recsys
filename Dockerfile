FROM python:3.11-slim

WORKDIR /app

ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /app

RUN pip install '.'

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the command to start your application
CMD ["hits-recsys_server", "--host","0.0.0.0"]