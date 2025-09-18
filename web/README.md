# Calby Web

This is the frontend for the Calby voice agent application, built with Next.js and `bun`.

## Prerequisites

- [Bun](https://bun.sh/) installed on your system.

## Setup

1.  **Install dependencies:**

    ```bash
    bun install
    ```

2.  **Create a `.env.local` file:**
    Copy the contents of `.env.example` to a new file named `.env.local` and fill in the required LiveKit API keys and secrets.

3.  **Run the development server:**
    ```bash
    bun run dev
    ```
    The application will be available at `http://localhost:3000`.

## Important Information

- This project uses `shadcn/ui` for components. To add new components, you can run:
  ```bash
  bunx shadcn-ui@latest add [component-name]
  ```
- The frontend is configured to communicate with the API running on `http://127.0.0.1:8000`. Ensure the API is running before starting the frontend.
- The `dev` script uses Next.js with Turbopack for faster development.

## Project Structure

- **`app/`**: Contains the main application routes and pages.
- **`components/`**: Contains the React components used throughout the application.
- **`hooks/`**: Contains custom React hooks.
- **`lib/`**: Contains utility functions and type definitions.
- **`public/`**: Contains static assets.
- **`package.json`**: Defines the project dependencies and scripts.
- **`.env.example`**: An example environment file.
