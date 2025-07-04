import gradio as gr
import os
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
import json
import google.genai as genai
from google.genai import types

# Initialize MCP Client
mcp_client = Client(StreamableHttpTransport("http://mcp-server:8001/mcp/"))

# Configure Google Generative AI
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options=types.HttpOptions(api_version='v1alpha')
)

async def llm_to_mcp_request(natural_language_question: str, prompt_name: str = "nl_to_mcp_tool_prompt") -> dict:
    """
    Uses an LLM to convert a natural language question
    into a structured MCP request for the 'query_database' tool.
    """
    try:

        # Fetch the prompt from the MCP server
        async with mcp_client:
            prompt_result = await mcp_client.get_prompt(prompt_name, arguments={"natural_language_question": natural_language_question})

        final_prompt = str(prompt_result.messages[0].content.text)
        # Make the LLM API call
        response = client.models.generate_content(model='gemini-2.5-pro', contents=final_prompt)

        llm_output_text = str(response.text).strip()
        # Extract JSON from markdown code block if present
        import re
        match = re.search(r'```json\n(.*)\n```', llm_output_text, re.DOTALL)
        if match:
            llm_output_text = match.group(1).strip()
        print(f"LLM Raw Output: '{response.text}'")
        print(f"LLM Stripped Output: '{llm_output_text}'")

        # Attempt to parse the LLM's JSON output
        try:
            parsed_response = json.loads(llm_output_text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Problematic JSON string: '{llm_output_text}'")
            raise # Re-raise the exception to propagate the error
        return parsed_response
    except Exception as e:
        print(f"Error generating or parsing LLM response: {e}")
        # Fallback to a default query in case of LLM error or invalid JSON
        return {"tool_name": "query_database", "args": {"table_name": "customer", "limit": 10}}

async def process_question(natural_language_question: str) -> str:
    """
    Processes the natural language question, converts it to an MCP request,
    sends it to the MCP server, and returns the result.
    """
    try:
        # Determine which prompt to use based on the question
        if "summarize" in natural_language_question.lower() and "results" in natural_language_question.lower():
            # This path would be taken if the user explicitly asks for a summary of previous results
            # For now, we'll just proceed with a query and then summarize its results.
            # In a more advanced agent, you might have a state to remember previous results.
            pass # Continue to query

        # Step 1: Use LLM to get MCP request for query_database tool
        mcp_request = await llm_to_mcp_request(natural_language_question, prompt_name="nl_to_mcp_tool_prompt")
        tool_name = mcp_request.get("tool_name")
        tool_args = mcp_request.get("args", {})

        if not tool_name:
            return json.dumps({"status": "error", "message": "LLM did not provide a tool name.", "data": {}})

        # Step 2: Send request to MCP server
        import asyncio
        await asyncio.sleep(1) # Give the server a moment to fully start
        async with mcp_client:
            response = await mcp_client.call_tool(tool_name, tool_args)
        print(f"MCP Client Response Type: {type(response)}")
        print(f"MCP Client Response: {response}")
        
        # Step 3: Format and return the response
        if response.content is not None:
            data = response.content
            if data is None:
                final_response = {"status": "success", "message": "Query returned no data.", "data": []}
            else:
                # If the user asked for a summary, use the summarization prompt
                if "summarize" in natural_language_question.lower() and "results" in natural_language_question.lower():
                    summary_prompt_result = await mcp_client.get_prompt("summarize_query_results_prompt", query_results=json.dumps(data))
                    summary_prompt = summary_prompt_result.content
                    llm_summary_response = client.generate_content(contents=summary_prompt)
                    final_response = {"status": "success", "message": "Query successful and summarized.", "data": str(llm_summary_response.text).strip()}
                else:
                    final_response = {"status": "success", "message": "Query successful.", "data": str(data)}
            return json.dumps(final_response)
        else:
            return json.dumps({"status": "error", "message": response.content or "Unknown error from MCP server."})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return json.dumps({"status": "error", "message": f"An error occurred: {str(e)}"})



# Gradio Interface
iface = gr.Interface(
    fn=process_question,
    inputs=gr.Textbox(lines=2, placeholder="Ask a question about the TPC-H database..."),
    outputs="json",
    title="TPC-H Database Query (LLM + MCP)",
    description="Enter a natural language question to query the TPC-H database via an LLM and MCP server.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
