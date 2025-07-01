# TPC-H Flask API

This is a REST API for the TPC-H benchmark, built with Flask and PostgreSQL.

## Setup

1.  **Install Dependencies**: This project uses `uv` for package management. To install the required packages, run:

    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Set up the Database**: 
    *   Make sure you have PostgreSQL installed and running.
    *   Create a new database named `tpch`.
    *   Set the `DATABASE_URL` environment variable to point to your database. For example:

        ```bash
        export DATABASE_URL="postgresql://user:password@localhost/tpch"
        ```

3.  **Run the Application**:

    ```bash
    python run.py
    ```

    The application will be available at `http://127.0.0.1:5000`.
