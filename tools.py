"""
tools.py
Defines the tools available to Param's digital twin agent.

Tools:
1. calculator       – evaluates safe math expressions
2. web_search       – DuckDuckGo live web search
3. get_current_datetime – returns today's date & time
"""

import math
import datetime
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
    Use this for any arithmetic, percentages, or simple math.
    Example: '2 ** 10', '(500 * 0.18)', 'math.sqrt(144)'
    """
    try:
        # Safe evaluation – only allow math ops
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        allowed_names["abs"] = abs
        allowed_names["round"] = round
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return f"Result: {result}"
    except Exception as e:
        return f"Calculator error: {e}"

_ddg = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """
    Searches the web using DuckDuckGo and returns a brief summary.
    Use this for current events, tech news, job market info, or anything
    that requires up-to-date information from the internet.
    """
    try:
        result = _ddg.run(query)
        return result if result else "No results found."
    except Exception as e:
        return f"Search error: {e}"


@tool
def get_current_datetime(dummy: str = "") -> str:
    """
    Returns the current date and time in IST (Indian Standard Time).
    Use this whenever the user asks what time or date it is.
    The 'dummy' parameter is unused – pass an empty string.
    """
    now = datetime.datetime.now()
    return now.strftime("Today is %A, %B %d, %Y. Current time: %I:%M %p")


ALL_TOOLS = [calculator, web_search, get_current_datetime]
