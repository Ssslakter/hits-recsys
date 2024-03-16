FROM python:3.11-slim

WORKDIR /app

# choose correct torch based on device
RUN if command -v nvidia-smi &> /dev/null; then \
    pip install torch --index-url https://download.pytorch.org/whl/cu121; \
else \
    pip install torch; \
fi

ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /app

RUN pip install '.'

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the command to start your application
CMD ["hits-recsys_server", "--host","0.0.0.0"]