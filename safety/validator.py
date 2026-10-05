from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of checking an agent action."""

    allowed: bool
    reason: str


class SafetyValidator:
    """Validates actions before they reach real tools."""

    BLOCKED_ACTIONS = {
        "delete_file",
        "delete_all",
        "execute_command",
    }

    def validate(self, action: str, parameters: dict) -> ValidationResult:
        """Check whether an action is safe to execute."""

        if action in self.BLOCKED_ACTIONS:
            return ValidationResult(
                allowed=False,
                reason=(
                    f"Action '{action}' is potentially destructive "
                    "and requires explicit approval."
                ),
            )

        if action == "move_file":
            source = parameters.get("source", "")
            destination = parameters.get("destination", "")

            if not source or not destination:
                return ValidationResult(
                    allowed=False,
                    reason="Source and destination are required.",
                )

        return ValidationResult(
            allowed=True,
            reason="Action passed safety validation.",
        )
