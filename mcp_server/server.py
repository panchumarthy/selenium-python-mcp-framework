"""
MCP server that exposes Selenium browser actions as tools for Claude to call.
Run this server standalone: python -m mcp_server.server
"""

import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp_server.browser_tools as bt

app = Server("selenium-browser")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="start_browser",
            description="Start a Chrome browser session. Call this before any other browser tool.",
            inputSchema={
                "type": "object",
                "properties": {
                    "headless": {"type": "boolean", "description": "Run browser in headless mode (no UI). Default false."}
                },
            },
        ),
        Tool(
            name="stop_browser",
            description="Close the browser and end the session.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="navigate_to",
            description="Navigate the browser to a URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Full URL to navigate to"}
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="get_page_text",
            description="Get all visible text from the current page body. Use to read page content and understand what's on screen.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_page_source",
            description="Get the HTML source of the current page (first 8000 chars). Use to find element selectors.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="find_elements",
            description="Find elements on the page by CSS selector, XPath, id, name, class, or tag. Returns list of matching elements with their text.",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "The selector string"},
                    "by": {
                        "type": "string",
                        "enum": ["css", "xpath", "id", "name", "class", "tag", "text"],
                        "description": "Selector strategy. Default: css",
                    },
                },
                "required": ["selector"],
            },
        ),
        Tool(
            name="click_element",
            description="Click an element on the page. Scrolls element into view before clicking.",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "Selector for the element"},
                    "by": {"type": "string", "enum": ["css", "xpath", "id", "name", "class"], "description": "Selector strategy"},
                    "index": {"type": "integer", "description": "Index if multiple elements match. Default 0."},
                },
                "required": ["selector"],
            },
        ),
        Tool(
            name="fill_input",
            description="Type text into an input field or textarea.",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "Selector for the input element"},
                    "value": {"type": "string", "description": "Text to type"},
                    "by": {"type": "string", "enum": ["css", "xpath", "id", "name"], "description": "Selector strategy"},
                    "clear_first": {"type": "boolean", "description": "Clear existing text before typing. Default true."},
                },
                "required": ["selector", "value"],
            },
        ),
        Tool(
            name="press_key",
            description="Press a keyboard key on a focused element (enter, tab, escape).",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string"},
                    "key": {"type": "string", "enum": ["enter", "tab", "escape"]},
                    "by": {"type": "string", "enum": ["css", "xpath", "id"]},
                },
                "required": ["selector", "key"],
            },
        ),
        Tool(
            name="get_element_attribute",
            description="Get the value of an HTML attribute on an element (e.g. href, value, class, data-*).",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string"},
                    "attribute": {"type": "string", "description": "Attribute name to read"},
                    "by": {"type": "string", "enum": ["css", "xpath", "id", "name"]},
                },
                "required": ["selector", "attribute"],
            },
        ),
        Tool(
            name="take_screenshot",
            description="Take a screenshot of the current page and save it to the screenshots/ folder.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Filename for the screenshot (e.g. login.png)"}
                },
            },
        ),
        Tool(
            name="get_current_url",
            description="Get the current URL and page title.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="wait_for_element",
            description="Wait until an element is visible on the page (useful after navigation or form submit).",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string"},
                    "by": {"type": "string", "enum": ["css", "xpath", "id"]},
                    "timeout": {"type": "integer", "description": "Max seconds to wait. Default 10."},
                },
                "required": ["selector"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    tool_map = {
        "start_browser": lambda a: bt.start_browser(**a),
        "stop_browser": lambda a: bt.stop_browser(),
        "navigate_to": lambda a: bt.navigate_to(**a),
        "get_page_text": lambda a: bt.get_page_text(),
        "get_page_source": lambda a: bt.get_page_source(),
        "find_elements": lambda a: bt.find_elements(**a),
        "click_element": lambda a: bt.click_element(**a),
        "fill_input": lambda a: bt.fill_input(**a),
        "press_key": lambda a: bt.press_key(**a),
        "get_element_attribute": lambda a: bt.get_element_attribute(**a),
        "take_screenshot": lambda a: bt.take_screenshot(**a),
        "get_current_url": lambda a: bt.get_current_url(),
        "wait_for_element": lambda a: bt.wait_for_element(**a),
    }

    handler = tool_map.get(name)
    if not handler:
        result = {"status": "error", "message": f"Unknown tool: {name}"}
    else:
        try:
            result = handler(arguments)
        except Exception as e:
            result = {"status": "error", "message": str(e)}

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
