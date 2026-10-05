from pathlib import Path


class ReportTool:
    """Create reports inside the sandbox."""

    def __init__(self, sandbox: str = "sandbox/files"):
        self.sandbox = Path(sandbox).resolve()

    def write_report(self, path: str, content: str) -> str:
        """Write a Markdown report inside the sandbox."""

        destination = (self.sandbox / path).resolve()

        if self.sandbox not in destination.parents:
            raise ValueError("Access outside the sandbox is not allowed.")

        if destination.suffix.lower() != ".md":
            raise ValueError("Reports must use the .md extension.")

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

        return f"Report created successfully: {path}"
