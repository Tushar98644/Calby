# Calby Architecture Overview

This document provides a comprehensive overview of the Calby voice agent application's architecture, covering both the frontend and backend components. The application is designed to be a scalable, real-time platform for AI-powered customer support.

## High-Level Architecture

Calby operates on a client-server model, composed of two main parts:

1.  **Backend (`api/`)**: A Python-based application built with **FastAPI**. It orchestrates real-time communication, manages AI agent logic, and handles call lifecycle events.
2.  **Frontend (`web/`)**: A modern web application built with **Next.js** and **React**. It provides the user interface for interacting with the voice agent.

These two components communicate with each other and with several external services to deliver a seamless experience.

![High-Level Architecture Diagram](https://raw.githubusercontent.com/livekit-examples/calby/main/docs/calby-high-level.png)

### Core Technologies

- **Real-time Communication**: [LiveKit](https://livekit.io/) is used for robust, low-latency audio and video call capabilities.
- **AI and Language Models**: [LangChain](https://www.langchain.com/) and [Google Gemini](https://deepmind.google/technologies/gemini/) provide the foundation for the intelligent support and specialist agents.
- **Speech-to-Text (STT)**: [Deepgram](https://deepgram.com/) for accurate real-time transcription.
- **Text-to-Speech (TTS)**: [Cartesia](https://www.cartesia.ai/) for natural-sounding AI-generated speech.

## Backend Architecture (`api/`)

The backend is a high-performance FastAPI application responsible for all server-side logic.

![Backend Architecture Diagram](https://raw.githubusercontent.com/livekit-examples/calby/main/docs/calby-backend.png)

### Key Components:

1.  **FastAPI Application (`app/`)**:

    - **Routers (`app/routers/`)**: Defines the API endpoints. The primary endpoint is for creating a `LiveKit` token to allow a client to connect to a room.
    - **Services (`app/services/`)**: Contains the business logic.
      - `livekit_service.py`: Interacts with the LiveKit server-side SDK to create rooms and generate tokens.
      - `transfer_service.py`: Manages the logic for "warm transfers" between the support and specialist agents.

2.  **LiveKit Agents (`agents/`)**:

    - This is the core of the AI functionality, where the voice agents are defined. The agents are built using the `livekit-agents` Python SDK.
    - **Support Agent (`agents/livekit_agents/support_agent.py`)**: The first point of contact for the user. It listens to the user, transcribes their speech using Deepgram, and uses a LangGraph workflow to decide if a transfer is needed.
    - **Specialist Agent (`agents/livekit_agents/specialist_agent.py`)**: A second-level agent that handles more complex queries. It receives context from the support agent during a transfer.
    - **Agent Entrypoints (`run_support.py`, `run_specialist.py`)**: These scripts are the entry points for running the agent workers. They connect to the LiveKit room and wait for jobs.

3.  **LangGraph Workflows (`agents/langgraph_agents/`)**:

    - LangGraph is used to define the conversational flow and decision-making logic for the agents as a state machine.
    - **State (`state.py`)**: Defines the conversation state, which includes the history of messages.
    - **Nodes (`nodes.py`)**: These are the steps in the graph. For example, `decide_transfer_node` uses the Gemini LLM to analyze the conversation and determine if a transfer is necessary.
    - **Workflows (`workflows/`)**: Defines the structure of the agent's logic, connecting the nodes into a coherent flow.

4.  **Configuration and Dependencies**:
    - **`.env`**: Manages all API keys and secrets for external services.
    - **`pyproject.toml`**: Defines project metadata and Python dependencies.

## Frontend Architecture (`web/`)

The frontend is a responsive and interactive user interface built with Next.js.

![Frontend Architecture Diagram](https://raw.githubusercontent.com/livekit-examples/calby/main/docs/calby-frontend.png)

### Key Components:

1.  **Next.js Application (`app/`)**:

    - Uses the App Router for file-based routing.
    - The main entry point is `app/(app)/page.tsx`, which renders the main `<App />` component.
    - `layout.tsx` defines the root layout, including fonts, theme settings, and metadata.

2.  **React Components (`components/`)**:

    - **UI Components (`components/ui/`)**: A set of reusable UI components built using `shadcn/ui`, such as buttons, selects, and toggles.
    - **LiveKit Components (`components/livekit/`)**: These components integrate directly with the LiveKit client SDKs (`@livekit/components-react`).
      - `device-select.tsx`: Allows users to select their microphone and camera.
      - `track-toggle.tsx`: Enables/disables media tracks.
      - `agent-control-bar.tsx`: The main control bar for muting, screen sharing, and ending the call.
      - `chat/`: Components for the real-time chat/transcription view.
    - **Core Components (`app.tsx`, `session-view.tsx`)**: These components manage the main application state and orchestrate the user session.

3.  **Hooks (`hooks/`)**:

    - Contains custom React hooks for managing state and side effects.
    - `useChatAndTranscription.ts`: A key hook that merges incoming chat messages and live transcriptions into a single, sorted list for display.
    - `useConnectionDetails.ts`: Manages the logic for connecting to the backend to get a LiveKit token and establishing a connection to the LiveKit room.

4.  **Styling**:

    - **Tailwind CSS**: Used for utility-first styling. The configuration is in `tailwind.config.ts`.
    - **Global Styles (`app/globals.css`)**: Defines CSS variables for theming (light and dark modes) and other base styles.

5.  **Configuration and Dependencies**:
    - **`.env.local`**: Stores frontend-specific environment variables, such as the LiveKit URL.
    - **`package.json`**: Manages all Node.js dependencies.
    - **`app-config.ts`**: Defines default configuration values for the UI, such as titles and logos, which can be overridden remotely.
