# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY ./app ./app
COPY ./model ./model
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
