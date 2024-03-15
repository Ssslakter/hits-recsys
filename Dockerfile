FROM python:3.11-slim-buster

WORKDIR /app
ADD . /app


RUN pip install '.'

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start your application
CMD ["hits-recsys", "--help"]