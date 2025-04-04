# OpenAI Assistant Streamlit

A Streamlit application that integrates with OpenAI's Assistant API.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for Docker setup)
- OpenAI API key
- OpenAI Assistant ID

## Environment Setup

1. Clone the repository
```bash
git clone https://github.com/allseeteam/openai-assistant-streamlit
cd openai-assistant-streamlit
```

2. Create .env file from example
```bash
cp .env.example .env
```

3. Configure the .env file with your settings:
```ini
# OpenAI Configuration
OPENAI_API_KEY="your-api-key"
OPENAI_ASSISTANT_ID="your-assistant-id"
# OPENAI_PROXY_URL="your-proxy-url"  # Optional: Proxy URL for OpenAI API requests

# Streamlit System Settings
STREAMLIT_SYSTEM_PORT=8501
STREAMLIT_SYSTEM_PASSWORD=your-password

# Streamlit Text Settings
STREAMLIT_TEXTS_PASSWORD_REQUEST="Enter password"
STREAMLIT_TEXTS_PASSWORD_INCORRECT="Incorrect password"
STREAMLIT_TEXTS_TITLE="Demo Application"
STREAMLIT_TEXTS_CHAT_INPUT="Enter message"
```

## Local Development Setup

1. Create and activate Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python -m streamlit run src/app.py
```

The application will be available at `http://localhost:8501` (or your configured port)

## Docker Setup

1. Build and start the container (using environment variables for port mapping)
```bash
docker compose --env-file .env up --build
```

The application will be available at `http://localhost:8501` (or your configured port)

2. Stop the application
```bash
docker compose down
```

3. View logs
```bash
docker compose logs -f
```

## Development

To modify the application:
1. For local development, make changes and Streamlit will automatically reload
2. For Docker setup, rebuild the container after changes:
```bash
docker compose --env-file .env up --build
