# Use Python image
FROM python:3.12.7

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI (optional, if you need to retrieve secrets using AWS CLI)
RUN apt-get update && apt-get install -y \
    awscli \
    && rm -rf /var/lib/apt/lists/*

# Expose the Streamlit default port
EXPOSE 8501

# Command to run the Streamlit app
# IMPORTANT: Don't pass environment variables here directly.
CMD ["python", "-m", "streamlit", "run", "Home.py"]
