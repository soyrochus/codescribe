# CodeScribe

> **Note:** CodeScribe is intended as an example project for how to create MCP servers in both JavaScript and Python. The project is in a very early, experimental phase. It demonstrates both deterministic tools and tools that use AI, and will likely include additional features such as resource management in the future.

## About This Project

CodeScribe is an educational example of how to build [Model Context Protocol (MCP)](https://modelcontext.org/) servers in both JavaScript and Python. It is intended for developers interested in agent tool design, MCP integration, and hybrid deterministic/AI workflows.

## Features

- **Journaling:** Log free-form notes, ideas, reminders, and comments to a daily journal file.
- **Summarization:** Use OpenAI to summarize a day's journal entries.
- **Categorization:** Use OpenAI to tag/categorize journal entries by theme (e.g., bug, idea, decision, question).
- **MCP Server:** Exposes tools via MCP protocol for integration with compatible hosts (e.g., VS Code, custom clients).
- **Command-Line Interface:** All tools are available via CLI for quick local use.
- **Extensible:** Designed to be extended with new tools, including deterministic and AI-powered ones.

## How It Works

- Journal entries are appended to `.journal/YYYY-MM-DD.txt` in your project root.
- Each entry is timestamped: `[HH:MM:SS] your note here`
- Summarization and categorization use OpenAI's GPT models (requires API key).

## Extending CodeScribe

You can add new tools by editing `codescribe/agent.py` (Python) or `codescribe-agent.js` (JavaScript). Tools can be deterministic (pure code) or use AI models. See the source for examples of both.

## Troubleshooting

- **Missing API Key:** Ensure `OPENAI_API_KEY` is set in your `.env` or environment.
- **MCP Not Connecting:** Check your `.vscode/mcp.json` configuration and that only one agent is running at a time.
- **Python Dependencies:** Use `uv sync` to install all required packages.

## Resources

- [Model Context Protocol (MCP)](https://modelcontext.org/)
- [LangChain.js](https://js.langchain.com/)
- [LangChain Python](https://python.langchain.com/) (Not used in the Python example)
- [OpenAI API](https://platform.openai.com/docs/api-reference)

## Install

### JavaScript version
```bash
npm install
```
Uses LangChain.js together with the MCP SDK.

### Python version
```bash
uv sync
```

For node.js we use the default npm package manager. For Pyhthon you will need to install [Uv](https://docs.astral.sh/uv/)

## Run

### JavaScript
Start the MCP server with:
```bash
node codescribe-agent.js mcp
```

### Python
Start the Python server with:
```bash
python -m codescribe mcp
```

Each version listens on stdin/stdout so it can be invoked by any MCP-compliant host. Entries are appended to `.journal/YYYY-MM-DD.txt` in the form `[HH:MM:SS] message`.

Once running, send an MCP `callTool` request with your instruction. The agent logs the note and returns a confirmation message.

### Command line usage

The Python version can run tools directly from the command line:

```bash
python -m codescribe log "my note here"
python -m codescribe summarize        # summarize today's journal
python -m codescribe summarize 2024-05-01
python -m codescribe tag 2024-05-01   # categorize entries
python -m codescribe mcp              # start MCP server
```

For the Javascript version you need to use the same commands but using node to run the script, for example:

```bash
node codescribe-agent.js log "my note here"
# etc..
```

## MCP Server Configuration for VSCode

Add the following to `.vscode/mcp.json` depending on the implementation you want to run:

```json
{
    "servers":{
        "codescribe-js": {
            "type": "stdio",
            "command": "node",
            "args": ["./codescribe-agent.js"]
        },
         "codescribe-py": {
            "type": "stdio",
            "command": "uv",
            "args": ["run", 
                "--directory", 
                "${workspaceFolder}",
                "-m",
                "codescribe",
                "run"
            ]
        }
    }
}
```

This configuration ensures the Python agent is started correctly as an MCP server using `uv`.

This tells your MCP-compatible tools how to launch the agent locally. Make sure the `.vscode/mcp.json` file is located in the project root. Only use one of the two implementation as otherwise Github Copilot might get confused about which Agent to run.


## Configuration

1. Create a `.env` file in the project root containing your OpenAI API key:

   ```dotenv
   OPENAI_API_KEY=your_key_here
   ```

2. Alternatively, set the `OPENAI_API_KEY` environment variable:

   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

## License and Copyright

Copyright (c) 2025, Iwan van der Kleijn

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
