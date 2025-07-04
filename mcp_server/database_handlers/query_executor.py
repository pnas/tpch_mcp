import os
import psycopg2
from psycopg2 import Error
import json # To parse/return JSON data

def execute_query_prompt(prompt_arguments: dict) -> dict:
    """
    Executes a database query based on structured prompt arguments.
    Returns results in a structured dictionary.
    """
    table_name = prompt_arguments.get("table_name")
    select_columns = prompt_arguments.get("select_columns", ["*"])
    where_conditions = prompt_arguments.get("where_conditions", [])
    order_by = prompt_arguments.get("order_by")
    limit = prompt_arguments.get("limit")
    join_tables = prompt_arguments.get("join_tables", [])
    join_conditions = prompt_arguments.get("join_conditions", [])

    if not table_name:
        return {"status": "error", "message": "table_name is required."}

    connection = None
    try:
        database_url = os.environ.get("DATABASE_URL")
        print(f"Attempting to connect to database with URL: {database_url}") # Debugging line
        if not database_url:
            return {"status": "error", "message": "DATABASE_URL environment variable not set."}
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()

        # Build the SQL query dynamically and safely
        columns_str = ", ".join(select_columns)
        sql = f"SELECT {columns_str} FROM {table_name}"

        for i, join_table in enumerate(join_tables):
            if i < len(join_conditions):
                sql += f" JOIN {join_table} ON {join_conditions[i]}"

        params = []
        if where_conditions:
            # IMPORTANT: For real-world security, you'd parse and validate
            # these conditions more rigorously to prevent arbitrary SQL.
            # This example assumes conditions are simple and safe literals
            # or uses placeholders for complex values if they came from user input.
            sql += " WHERE " + " AND ".join(where_conditions)
            # If where_conditions contained values, you'd add them to params list:
            # for condition in where_conditions:
            #     if 'value_placeholder' in condition:
            #         params.append(actual_value_from_args)


        if order_by:
            sql += f" ORDER BY {order_by}" # Be careful with order_by injection! Validate input.

        if limit is not None:
            sql += " LIMIT %s"
            params.append(limit)

        print(f"MCP Server preparing SQL: {sql} with params: {params}") # For debugging
        cursor.execute(sql, tuple(params))

        # Fetch results and column names
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        # Format results into a list of dictionaries for easier consumption by clients
        results = []
        for row in rows:
            results.append(dict(zip(column_names, row)))

        return {
            "status": "success",
            "message": f"Successfully queried {len(results)} rows from {table_name}.",
            "data": results,
            "column_names": column_names
        }

    except (Exception, Error) as error:
        print(f"Error during MCP database query: {error}")
        return {"status": "error", "message": f"Database query failed: {error}"}
    finally:
        if connection:
            cursor.close()
            connection.close()

# This function would be called by the MCP server's core logic
# if __name__ == "__main__":
#     # Example direct call for testing within the server's context
#     test_args = {
#         "table_name": "products",
#         "select_columns": ["name", "price"],
#         "where_conditions": ["price < 100.00", "stock_quantity > 0"],
#         "order_by": "price DESC",
#         "limit": 5
#     }
#     result = execute_query_prompt(test_args)
#     print(json.dumps(result, indent=2))