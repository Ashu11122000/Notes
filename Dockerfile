# Base image 
# Using Python 3.12 as the base image for our FastAPI application
FROM python:3.12

# Set working directory to /app for the application
WORKDIR /app

# Copy requirements file to the working directory
COPY requirements.txt .

# Install dependencies from requirements.txt using uv and pip
RUN uv pip freeze > requirements.txt

# Copy project files to the working directory
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run app using uvicorn with specified host and port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]