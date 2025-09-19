# Setup Guide

This guide provides step-by-step instructions for setting up and running the Calby application locally.

## Prerequisites

- [Python](https://www.python.org/downloads/) (3.11 or higher)
- [Node.js](https://nodejs.org/en) (v18 or higher)
- [Bun](https://bun.sh/) (for the frontend)
- [uv](https://github.com/astral-sh/uv) (for the backend Python environment)
- Access keys for:
  - LiveKit
  - Google Gemini
  - Deepgram
  - Cartesia

## 1. Backend Setup (`api/`)

The backend is a Python application powered by FastAPI.

### Step 1: Set up the Environment

Navigate to the `api` directory:

```bash
cd api
```

Create a virtual environment and install the required Python packages using `uv`:

```bash
# Create the virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from uv.lock
uv pip sync
```

### Step 2: Configure Environment Variables

Create a `.env` file in the `api/` directory by copying the example file if one exists, or creating a new one. Add the following variables:

```env
# LiveKit Credentials
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=

# AI Service Keys
GOOGLE_API_KEY=
DEEPGRAM_API_KEY=
CARTESIA_API_KEY=
```

### Step 3: Run the Backend Services

You need to run three separate processes for the backend: the FastAPI server and the two AI agent workers.

**Terminal 1: Run the FastAPI Server**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2: Run the Support Agent Worker**

```bash
python -m agents.run_support
```

**Terminal 3: Run the Specialist Agent Worker**

```bash
python -m agents.run_specialist
```

## 2. Frontend Setup (`web/`)

The frontend is a Next.js application.

### Step 1: Install Dependencies

Navigate to the `web` directory:

```bash
cd web
```

Install the Node.js dependencies using `bun`:

```bash
bun install
```

### Step 2: Configure Environment Variables

Create a `.env.local` file in the `web/` directory. You will need to add the URL for your LiveKit instance:

```env
NEXT_PUBLIC_LIVEKIT_URL=
```

### Step 3: Run the Frontend Development Server

```bash
bun dev
```

Once all services are running, you can access the application in your browser at `http://localhost:3000`.
