import json
from typing import Any, Callable

from openai import OpenAI


class Agent:
    """A lightweight tool-using AI agent."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.tools: dict[str, Callable[..., Any]] = {}

    def register_tool(
        self,
        name: str,
        function: Callable[..., Any],
        description: str,
        parameters: dict,
    ) -> None:
        """Register a function the agent can call."""

        self.tools[name] = {
            "function": function,
            "description": description,
            "parameters": parameters,
        }

    def _tool_definitions(self) -> list[dict]:
        """Convert registered tools into the format expected by the model."""

        definitions = []

        for name, tool in self.tools.items():
            definitions.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool["description"],
                        "parameters": tool["parameters"],
                    },
                }
            )

        return definitions

    def _execute_tool(self, name: str, arguments: str) -> str:
        """Execute a registered tool."""

        if name not in self.tools:
            return f"Error: unknown tool '{name}'."

        try:
            parsed_arguments = json.loads(arguments)

            result = self.tools[name]["function"](**parsed_arguments)

            return str(result)

        except Exception as error:
            return f"Tool error: {error}"

    def run(self, task: str) -> str:
        """Run the agent until it produces a final answer."""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI automation agent. "
                    "Break complex tasks into smaller steps. "
                    "Use tools when they are useful. "
                    "Never invent tool results."
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
                result = self._execute_tool(
                    tool_call.function.name,
                    tool_call.function.arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )
