import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai

# Try to load environment variables from either a provided path or a .env file
env_path = os.getenv("CODESCRIBE_ENV_PATH", Path(__file__).with_suffix(".env"))
load_dotenv(env_path)

openai_api_key = os.getenv("OPENAI_API_KEY")

DESCRIPTION = (
    "Adds a free-form note, idea, reminder, or comment to the developer's personal"
    " journal for this project (saved as a dated text file in the '.journal' folder).\n\n"
    "Use this tool to record:\n"
    "- Work-in-progress thoughts\n"
    "- Personal reminders\n"
    "- Design decisions\n"
    "- Reflections, doubts, or open questions\n"
    "- Context about why something was done\n"
    "- TODOs or things to revisit\n\n"
    "Trigger this tool with any natural instruction such as:\n"
    "- 'Add a note that...'\n"
    "- 'Remember to...'\n"
    "- 'Jot down...'\n"
    "- 'Make a comment about...'\n"
    "- 'Add to the project journal that...'\n\n"
    "Do not use this tool for adding documentation or comments inside the source code."
    " Use regular code comments or documentation blocks for that purpose.\n\n"
    "This journal is for personal context, process notes, or broader observations—"
    "anything you want to keep track of during development that doesn't belong directly"
    " in the codebase."
)


def log_note(note: str) -> str:
    """Append a note to today's journal file and return a confirmation."""
    if not note or not note.strip():
        raise ValueError("No note content provided")

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    journal_dir = Path.cwd() / ".journal"
    journal_dir.mkdir(exist_ok=True)
    file_path = journal_dir / f"{date_str}.txt"

    with file_path.open("a", encoding="utf-8") as f:
        f.write(f"[{time_str}] {note.strip()}\n")

    rel = file_path.relative_to(Path.cwd())
    return f"\U0001F4DD Logged note to {rel}"


def run_cli(text: str) -> None:
    """Process the user text through OpenAI and log the note."""
    if not openai_api_key:
        print("OPENAI_API_KEY missing. Add it to .env at", env_path, file=sys.stderr)
        sys.exit(1)

    client = openai.OpenAI(api_key=openai_api_key)

    functions = [
        {
            "name": "log_note",
            "description": DESCRIPTION,
            "parameters": {
                "type": "object",
                "properties": {"note": {"type": "string"}},
                "required": ["note"],
            },
        }
    ]

    messages = [
        {"role": "system", "content": "You are CodeScribe."},
        {"role": "user", "content": text},
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=0,
    )

    message = response.choices[0].message
    if message.function_call and message.function_call.name == "log_note":
        args = json.loads(message.function_call.arguments or "{}")
        note = args.get("note", text)
    else:
        note = text

    result = log_note(note)
    print(result)


async def start_server() -> None:
    """Start an MCP server exposing the `logNote` tool."""
    from mcp.server.mcp import McpServer  # type: ignore
    from mcp.server.stdio import StdioServerTransport  # type: ignore

    server = McpServer(
        name="CodeScribe",
        version="1.0.0",
        description=DESCRIPTION,
    )

    @server.tool("logNote", {"note": str})  # type: ignore
    async def log_note_tool(note: str):
        return {"content": [{"type": "text", "text": log_note(note)}]}

    transport = StdioServerTransport()
    await server.connect(transport)


def main() -> None:
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:]).strip()
        run_cli(text)
    else:
        import asyncio

        asyncio.run(start_server())


if __name__ == "__main__":
    main()
