# Extend the official Python image
FROM python:3.7.10-slim-buster

# Prepare app folder
WORKDIR /app

# Change back to root user to install dependencies
USER root

# Install packages from PyPI
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch back to non-root to run code
USER 1001

COPY . .

# Change back to root user to change folder owner
USER root

# Change owner of datastore folder
RUN chown 1001 /app/data/datastores

# Switch back to non-root to run code
USER 1001

EXPOSE 8080 8080

CMD [ "python3", "api.py"]