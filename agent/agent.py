import json
from typing import Any, Callable

from openai import OpenAI


class Agent:
    """A simple tool-using AI agent."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.tools: dict[str, Callable[..., Any]] = {}

    def register_tool(self, name: str, function: Callable[..., Any]) -> None:
        """Register a function that the agent can call."""
        self.tools[name] = function

    def run(self, task: str) -> str:
        """Run the agent on a task."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a tool-using automation agent. "
                    "Break tasks into small steps and use available tools "
                    "when necessary. Never invent tool results."
                ),
            },
            {
                "role": "user",
                "content": task,
            },
        ]

        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            message = response.choices[0].message

            if message.content:
                return message.content

            return "The agent completed without a final response."
