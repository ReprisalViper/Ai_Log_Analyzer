# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask pandas scikit-learn psycopg2-binary

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "Ai_Log_Analyzer.py"]
