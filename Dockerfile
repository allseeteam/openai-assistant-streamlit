# Use Python 3.11 slim image
FROM python:3.11-slim

# Define build argument
ARG STREAMLIT_SYSTEM_PORT

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/

# Expose the port (now using the ARG)
EXPOSE ${STREAMLIT_SYSTEM_PORT}

# Start the application (use shell form for environment variable expansion)
CMD ["sh", "-c", "python -m streamlit run src/app.py --server.port=$STREAMLIT_SYSTEM_PORT --server.address=0.0.0.0"]
