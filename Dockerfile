# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run Django migrations
RUN python manage.py migrate

# Specify the command to run on container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
