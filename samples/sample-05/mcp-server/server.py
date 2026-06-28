# MCP Server for Morning Briefing
# This is the data-fetching layer of your composed workflow

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("[TODO: your workflow name]")

# TODO: define your MCP tool here
# Example structure:
# @mcp.tool()
# def get_morning_inputs() -> dict:
#     """[TODO: describe what this tool does]"""
#     # TODO: implement the tool
#     pass

if __name__ == "__main__":
    mcp.run()
