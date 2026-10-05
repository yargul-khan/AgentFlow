from typing import Any, Callable

from safety.validator import SafetyValidator


class ToolManager:
    """Connects agent tool requests to tools and safety validation."""

    def __init__(self):
        self.validator = SafetyValidator()
        self.tools: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        function: Callable[..., Any],
        description: str,
        parameters: dict,
    ) -> None:
        """Register a tool and its LLM schema."""

        self.tools[name] = {
            "function": function,
            "description": description,
            "parameters": parameters,
        }

    def execute(
        self,
        name: str,
        parameters: dict[str, Any],
    ) -> str:
        """Validate and execute a tool request."""

        validation = self.validator.validate(
            action=name,
            parameters=parameters,
        )

        if not validation.allowed:
            return f"BLOCKED: {validation.reason}"

        if name not in self.tools:
            return f"ERROR: Unknown tool '{name}'."

        try:
            result = self.tools[name]["function"](**parameters)
            return str(result)

        except Exception as error:
            return f"ERROR: {error}"
