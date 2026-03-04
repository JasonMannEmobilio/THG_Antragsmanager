# PseudoBacken Project

This project consists of a FastAPI backend and a Vue 3 (Vite + Tailwind) frontend.

## How to Start the Project

### Prerequisites
- Python 3.x
- Node.js & npm

### Backend
The backend serves the API and proxies requests to Xano.

1.  Navigate to the root directory: `cd PseudoBacken`
2.  Activate the virtual environment (if not already active):
    - Windows: `.\venv\Scripts\activate`
3.  Run the backend server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will be available at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

### Frontend
The frontend is a Vue 3 application built with Vite.

1.  Navigate to the frontend directory: `cd frontend`
2.  Install dependencies (first time only):
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## Environment Variables
Ensure you have a `.env` file in the `backend/` directory with the following content:
```env
XANO_API_BASE_URL=https://your-xano-instance.xano.io/api:your-workspace
```
