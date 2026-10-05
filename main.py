from agent.agent import Agent
from agent.tool_manager import ToolManager
from tools.csv_tools import CSVTool
from tools.filesystem import FileSystemTool
from tools.report import ReportTool


def build_agent() -> Agent:
    """Create and configure the AgentFlow agent."""

    tool_manager = ToolManager()

    filesystem = FileSystemTool()
    csv_tool = CSVTool()
    report_tool = ReportTool()

    tool_manager.register(
        name="list_files",
        function=filesystem.list_files,
        description="List files available inside the sandbox.",
        parameters={
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    )

    tool_manager.register(
        name="move_file",
        function=filesystem.move_file,
        description="Move a file to another location inside the sandbox.",
        parameters={
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Source file path.",
                },
                "destination": {
                    "type": "string",
                    "description": "Destination file path.",
                },
            },
            "required": ["source", "destination"],
            "additionalProperties": False,
        },
    )

    tool_manager.register(
        name="read_csv",
        function=csv_tool.read_csv,
        description="Read basic information about a CSV file.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "CSV file path inside the sandbox.",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    )

    tool_manager.register(
        name="analyze_csv",
        function=csv_tool.analyze_csv,
        description="Analyze a CSV file and identify statistical anomalies.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "CSV file path inside the sandbox.",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    )

    tool_manager.register(
        name="write_report",
        function=report_tool.write_report,
        description="Create a Markdown report inside the sandbox.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Markdown file path.",
                },
                "content": {
                    "type": "string",
                    "description": "Report content.",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
    )

    return Agent(tool_manager=tool_manager)


if __name__ == "__main__":
    agent = build_agent()

    task = (
        "Analyze production.csv. "
        "Identify any unusual machines and explain the findings."
    )

    result = agent.run(task)

    print("\n=== AgentFlow Result ===\n")
    print(result)
