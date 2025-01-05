# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and application code
COPY requirements.txt .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables to avoid buffering
ENV PYTHONUNBUFFERED=1

# Expose the port if necessary (optional)
EXPOSE 8000

# Command to run the bot
CMD ["python", "tailscale-discord-bot.py"]
