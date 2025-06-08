import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List, Any
from dotenv import load_dotenv
import openai

# Try to load environment variables from a .env file in the same directory as this script
env_path = Path(__file__).parent / ".env"
print (f"Loading environment variables from {env_path}")
load_dotenv(env_path)

openai_api_key = os.getenv("OPENAI_API_KEY")


def get_open_api(messages : List[dict[str, str]] ) -> Any:
    """Return a configured OpenAI client or raise if no API key."""
    if not openai_api_key:
        raise RuntimeError(
            f"OPENAI_API_KEY missing. Add it to .env at {env_path}"
        )
    client =  openai.OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0,
    )
    return response

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


def summarize_journal(day: str | None = None) -> str:
    """Summarize the journal entries for a given day using OpenAI."""
    date_str = day or datetime.now().strftime("%Y-%m-%d")
    file_path = Path.cwd() / ".journal" / f"{date_str}.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"Journal file {file_path} does not exist")
    text = file_path.read_text(encoding="utf-8")

    messages = [
        {"role": "system", "content": "Summarize the following journal entries."},
        {"role": "user", "content": text},
    ]
    response = get_open_api(messages)
    return response.choices[0].message.content.strip()


def categorize_journal(day: str | None = None) -> str:
    """Tag journal entries by theme using OpenAI."""
    date_str = day or datetime.now().strftime("%Y-%m-%d")
    file_path = Path.cwd() / ".journal" / f"{date_str}.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"Journal file {file_path} does not exist")
    text = file_path.read_text(encoding="utf-8")

    prompt = (
        "Tag or categorize each journal entry by theme such as bug, idea, "
        "decision, or question."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]

    response = get_open_api(messages)
    return response.choices[0].message.content.strip()


def run_cli(args: list[str]) -> None:
    """Run one of the available tools from the command line."""
    if not args or any(a in {"-h", "--help"} for a in args):
        print("Usage:")
        print("  python codescribe-agent.py log <text>")
        print("  python codescribe-agent.py summarize [day]")
        print("  python codescribe-agent.py tag [day]")
        print("  python codescribe-agent.py mcp")
        return

    command, *rest = args

    if command == "log":
        text = " ".join(rest).strip()
        print(log_note(text))
        return

    if command in {"summarize", "summary"}:
        day = rest[0] if rest else None
        print(summarize_journal(day))
        return

    if command in {"tag", "categorize", "categorise"}:
        day = rest[0] if rest else None
        print(categorize_journal(day))
        return

    print(f"Unknown command: {command}", file=sys.stderr)
    print("Use --help for usage.", file=sys.stderr)


def start_server() -> None:
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(
        name="Codescribe",
        version="1.0.0",
        description=DESCRIPTION
    )

    @mcp.tool()
    async def logNote(note: str):
        return {"content": [{"type": "text", "text": log_note(note)}]}

    @mcp.tool()
    async def summarizeJournal(day: str | None = None):
        return {"content": [{"type": "text", "text": summarize_journal(day)}]}

    @mcp.tool()
    async def categorizeJournal(day: str | None = None):
        return {"content": [{"type": "text", "text": categorize_journal(day)}]}

    mcp.run()


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        start_server()
    else:
        run_cli(sys.argv[1:])


if __name__ == "__main__":
    main()
