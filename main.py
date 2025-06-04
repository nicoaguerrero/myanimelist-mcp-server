from mcp.server.fastmcp import FastMCP
from tools.tools import register_tools

mcp = FastMCP("myanimelist")
register_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
