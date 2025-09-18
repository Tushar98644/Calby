# Calby API

This is the backend for the Calby voice agent application, built with FastAPI. It uses `uv` for package management and is designed to be run in a virtual environment.

## Prerequisites

- Python 3.13 or higher
- `uv` installed (`pip install uv`)

## Setup

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies using `uv`:**

    ```bash
    uv pip install -e .
    ```

3.  **Create a `.env` file:**
    Copy the contents of `.env.example` to a new file named `.env` and fill in the required API keys and secrets for LiveKit, Google, Deepgram, and Cartesia.

4.  **Run the FastAPI server:**

    ```bash
    fastapi dev app/main.py
    ```

    The API will be available at `http://127.0.0.1:8000`.

5.  **Run the agent workers:**
    In two separate terminal sessions (with the virtual environment activated), run the support and specialist agents:

    For the support agent:

    ```bash
    python -m agents.run_support
    ```

    For the specialist agent:

    ```bash
    python -m agents.run_specialist
    ```

## Project Structure

- **`app/`**: Contains the core FastAPI application, including routers, services, and configuration.
- **`agents/`**: Contains the LiveKit agent logic, including the support and specialist agents, and the LangGraph workflows.
- **`pyproject.toml`**: Defines the project dependencies and metadata.
- **`.env.example`**: An example environment file.
