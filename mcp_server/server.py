from fastmcp import FastMCP
import logging
from mcp_server.database_handlers import query_executor # Import the query_executor
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

mcp = FastMCP("my-database-server", version="1.0.0", host="0.0.0.0")

# Define a resource for the TPC-H schema
@mcp.resource("schema://tpch")
def get_tpch_schema() -> dict:
    """Provides a simplified overview of the TPC-H database schema."""
    return {
        "tables": [
            {"name": "region", "primary_key": "r_regionkey", "description": "Geographic regions"},
            {"name": "nation", "primary_key": "n_nationkey", "description": "Nations within regions"},
            {"name": "part", "primary_key": "p_partkey", "description": "Information about parts"},
            {"name": "supplier", "primary_key": "s_suppkey", "description": "Information about suppliers"},
            {"name": "partsupp", "primary_key": ["ps_partkey", "ps_suppkey"], "description": "Part-supplier relationships"},
            {"name": "customer", "primary_key": "c_custkey", "description": "Information about customers"},
            {"name": "orders", "primary_key": "o_orderkey", "description": "Customer orders"},
            {"name": "lineitem", "primary_key": ["l_orderkey", "l_linenumber"], "description": "Line items within orders"}
        ]
    }

# Define the prompt for the LLM to convert NL to MCP tool requests
@mcp.prompt("nl_to_mcp_tool_prompt")
def nl_to_mcp_tool_prompt(natural_language_question: str) -> str:
    """
    You are a helpful assistant that converts natural language questions
    into structured JSON requests for a database query tool.
    The tool is named "query_database" and accepts the following arguments:
    - table_name (string, required): The name of the table (e.g., 'customer', 'lineitem', 'orders', 'part', 'supplier', 'nation', 'region', 'partsupp').
    - select_columns (array of strings, optional): List of columns to select (e.g., ["c_name", "c_address"]). Default is ["*"].
    - where_conditions (array of strings, optional): SQL WHERE clause conditions (e.g., ["c_custkey = 1", "o_totalprice > 100.00"]).
    - order_by (string, optional): Column to order by (e.g., "c_name ASC", "o_orderdate DESC").
    - limit (integer, optional): Maximum number of rows to return.

    Convert the following question into a JSON object for the "query_database" tool.
    Ensure the output is ONLY the JSON object and nothing else.

    Question: {natural_language_question}

    Example JSON output:
    {{
      "tool_name": "query_database",
      "args": {{
        "table_name": "customer",
        "select_columns": ["c_name", "c_phone"],
        "where_conditions": ["c_nationkey = 1"],
        "limit": 10
      }}
    }}
    """
    return f"""
    You are a helpful assistant that converts natural language questions
    into structured JSON requests for a database query tool.
    The tool is named "query_database" and accepts the following arguments:
    - table_name (string, required): The name of the table (e.g., 'customer', 'lineitem', 'orders', 'part', 'supplier', 'nation', 'region', 'partsupp').
    - select_columns (array of strings, optional): List of columns to select (e.g., ["c_name", "c_address"]). Default is ["*"].
    - where_conditions (array of strings, optional): SQL WHERE clause conditions (e.g., ["c_custkey = 1", "o_totalprice > 100.00"]).
    - order_by (string, optional): Column to order by (e.g., "c_name ASC", "o_orderdate DESC").
    - limit (integer, optional): Maximum number of rows to return.

    Convert the following question into a JSON object for the "query_database" tool.
    Ensure the output is ONLY the JSON object and nothing else.

    Question: {natural_language_question}

    Example JSON output:
    {{
      "tool_name": "query_database",
      "args": {{
        "table_name": "customer",
        "select_columns": ["c_name", "c_phone"],
        "where_conditions": ["c_nationkey = 1"],
        "limit": 10
      }}
    }}
    """

# Define a prompt for summarizing query results
@mcp.prompt("summarize_query_results_prompt")
def summarize_query_results_prompt(query_results: str) -> str:
    """
    You are a helpful assistant that summarizes database query results.
    Summarize the following JSON data in a concise and human-readable way.

    JSON Data: {query_results}
    """
    return f"""
    You are a helpful assistant that summarizes database query results.
    Summarize the following JSON data in a concise and human-readable way.

    JSON Data: {query_results}
    """

# Register the database query tool
@mcp.tool(name="query_database")

def query_database_tool(table_name: str, select_columns: list = None, where_conditions: list = None, order_by: str = None, limit: int = None) -> dict:
    """Executes a SQL SELECT query on the TPC-H database and returns the results.

    Args:
        table_name (str): The name of the table to query (e.g., 'customer', 'lineitem', 'orders').
        select_columns (list, optional): A list of column names to select. Defaults to all columns if not provided.
        where_conditions (list, optional): A list of SQL WHERE clause conditions (e.g., 'c_custkey = 1', 'o_totalprice > 100.00'). Be careful with SQL injection!
        order_by (str, optional): The column to order the results by, optionally with 'ASC' or 'DESC' (e.g., 'c_name ASC', 'o_orderdate DESC').
        limit (int, optional): The maximum number of rows to return.

    Returns:
        dict: The result of the query, including status, message, and data.
    """
    prompt_arguments = {
        "table_name": table_name,
        "select_columns": select_columns if select_columns is not None else ["*"],
        "where_conditions": where_conditions if where_conditions is not None else [],
        "order_by": order_by,
        "limit": limit
    }
    return query_executor.execute_query_prompt(prompt_arguments)

if __name__ == "__main__":
    logger.info("Starting MCP Database Server...")
    app = mcp.http_app()
    logger.info("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
    logger.info("MCP Database Server stopped.")
