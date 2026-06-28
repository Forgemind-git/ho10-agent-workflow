# MCP Server for Lead Workflow
# This is the data-fetching layer of your composed workflow

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("[TODO: your workflow name]")

# TODO: define your MCP tool here
# Example structure:
# @mcp.tool()
# def enrich_lead(company_name: str) -> dict:
#     """[TODO: describe what this tool does]"""
#     # TODO: implement the tool
#     pass

if __name__ == "__main__":
    mcp.run()
