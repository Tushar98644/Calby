# Frontend Documentation

This document provides an overview of the frontend architecture and components for the Calby application.

## Table of Contents

- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Architecture Overview](#architecture-overview)
- [Component Flow Diagram](#component-flow-diagram)
- [Components](#components)
- [State Management](#state-management)
- [API Communication](#api-communication)
- [Styling](#styling)

## Project Structure

The frontend code is located in the `/web` directory. Here is a breakdown of the key folders:

- `/web/app`: Contains the main application pages and layouts (Next.js App Router).
- `/web/components`: Reusable React components used throughout the application.
- `/web/hooks`: Custom React hooks for managing logic and state.
- `/web/lib`: Utility functions and type definitions.
- `/web/public`: Static assets like fonts and images.

## Technologies Used

- **Framework**: [Next.js](https://nextjs.org/) (with App Router)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **UI Library**: [React](https://reactjs.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Real-time Communication**: [LiveKit](https://livekit.io/)
- **Animation**: [Framer Motion](https://www.framer.com/motion/)

## Architecture Overview

The frontend is a Next.js application that uses the App Router for routing and server-side rendering. The main entry point is `web/app/(app)/page.tsx`, which renders the main `App` component.

The `App` component manages the overall state of the application, including the LiveKit room connection and whether a session has started. It conditionally renders either the `Welcome` component or the `SessionView` component based on the session state.

The `SessionView` is the core of the application, displaying the media tiles, chat/transcription, and agent controls. It utilizes custom hooks like `useChatAndTranscription` and `useConnectionDetails` to manage the application's logic.

## Component Flow Diagram

![Component Architecture](assets/web_architecture.png)

## Components

The application is built using a component-based architecture. Key components include:

- **`App`**: The root component that manages the application state and LiveKit room connection.
- **`Welcome`**: The initial screen that prompts the user to start a call.
- **`SessionView`**: Manages the main session view, including video tiles and controls.
- **`MediaTiles`**: A container for the `AgentTile` and `AvatarTile` components.
- **`AgentTile`**: Displays the agent's video feed and information.
- **`AvatarTile`**: Displays the user's avatar when video is disabled.
- **`AgentControlBar`**: Provides controls for the user to interact with the agent (e.g., mute, screen share).
- **`ChatMessageView`**: Displays the chat messages and transcriptions.
- **`ChatEntry`**: Renders a single chat message.

## State Management

Global state is managed using a combination of React Context (via `RoomContext` from LiveKit) and custom hooks.

- **`useConnectionDetails`**: Fetches and manages the connection details required to connect to the LiveKit room.
- **`useChatAndTranscription`**: Merges and manages the chat messages and real-time transcriptions from LiveKit.
- **`useDebugMode`**: A hook for enabling debug features in non-production environments.

## API Communication

The frontend communicates with the backend API for tasks such as fetching connection details. This is handled in `useConnectionDetails.ts` and the `/web/app/api` directory. The `useConnectionDetails` hook makes a request to the `/api/connection-details` endpoint to retrieve the LiveKit server URL and participant token.

## Styling

Styling is primarily done using Tailwind CSS. Global styles are defined in `/web/app/globals.css`. The `cn` utility from `lib/utils.ts` is used to conditionally apply classes.
