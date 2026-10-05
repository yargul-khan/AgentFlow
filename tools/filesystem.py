from pathlib import Path
import shutil


class FileSystemTool:
    """Safe file operations restricted to a sandbox directory."""

    def __init__(self, sandbox: str = "sandbox/files"):
        self.sandbox = Path(sandbox).resolve()
        self.sandbox.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, path: str) -> Path:
        """Return a path only if it stays inside the sandbox."""
        target = (self.sandbox / path).resolve()

        if self.sandbox not in target.parents and target != self.sandbox:
            raise ValueError("Access outside the sandbox is not allowed.")

        return target

    def list_files(self) -> list[str]:
        """List files inside the sandbox."""
        return [
            str(path.relative_to(self.sandbox))
            for path in self.sandbox.rglob("*")
            if path.is_file()
        ]

    def move_file(self, source: str, destination: str) -> str:
        """Move a file inside the sandbox."""
        source_path = self._safe_path(source)
        destination_path = self._safe_path(destination)

        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {source}")

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(destination_path))

        return f"Moved {source} to {destination}"
