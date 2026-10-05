import json
from typing import Any

from openai import OpenAI

from agent.tool_manager import ToolManager


class Agent:
    """A lightweight tool-using AI agent."""

    def __init__(
        self,
        tool_manager: ToolManager,
        model: str = "gpt-4o-mini",
    ):
        self.client = OpenAI()
        self.model = model
        self.tool_manager = tool_manager

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: dict,
    ) -> None:
        """Register a tool with the agent."""

        self.tool_manager.tools[name]["description"] = description
        self.tool_manager.tools[name]["parameters"] = parameters

    def _tool_definitions(self) -> list[dict]:
        """Build tool definitions for the LLM."""

        definitions = []

        for name, tool in self.tool_manager.tools.items():
            definitions.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool.get(
                            "description",
                            "No description provided.",
                        ),
                        "parameters": tool.get(
                            "parameters",
                            {
                                "type": "object",
                                "properties": {},
                            },
                        ),
                    },
                }
            )

        return definitions

    def run(self, task: str) -> str:
        """Run the agent until it produces a final answer."""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI automation agent. "
                    "Break complex tasks into smaller steps. "
                    "Use available tools when necessary. "
                    "Never invent tool results. "
                    "Only perform actions through the provided tools."
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
                tools=self._tool_definitions(),
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content or "The agent completed without a response."

            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                result = self.tool_manager.execute(
                    tool_name,
                    arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )
