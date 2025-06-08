# CodeScribe

> **Note:** CodeScribe is intended as an example project for how to create MCP servers in both JavaScript and Python. The project is in a very early stage. It will demonstrate both deterministic tools and tools that use AI, and will likely include additional features such as resource management in the future.

CodeScribe is a lightweight journaling agent that logs developer notes to daily files using natural language prompts. Notes are stored in a `.journal` folder relative to where you run the agent. Both a JavaScript and a Python implementation are provided.

## Install

### JavaScript version
```bash
npm install
```
Uses LangChain.js together with the MCP SDK.

### Python version
```bash
pip install -e .
```
Uses the `openai` package and the MCP Python SDK.

## Run

### JavaScript
Start the MCP server with:
```bash
node codescribe-agent.js
```

### Python
Start the Python server with:
```bash
python codescribe-agent.py mcp
```

Each version listens on stdin/stdout so it can be invoked by any MCP-compliant host. Entries are appended to `.journal/YYYY-MM-DD.txt` in the form `[HH:MM:SS] message`.

Once running, send an MCP `callTool` request with your instruction. The agent logs the note and returns a confirmation message.

### Command line usage

The Python version can run tools directly from the command line:

```bash
python codescribe-agent.py log "my note here"
python codescribe-agent.py summarize        # summarize today's journal
python codescribe-agent.py summarize 2024-05-01
python codescribe-agent.py tag 2024-05-01   # categorize entries
python codescribe-agent.py mcp              # start MCP server
```

## MCP Server Configuration (Development Mode)

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
                "${workspaceFolder}/codescribe-agent.py"
            ]
        }
    }
}
```

This tells your MCP-compatible tools how to launch the agent locally. Make sure the `.vscode/mcp.json` file is located in the project root.

## MCP Server Configuration (Python Agent)

To use the Python agent with MCP, add the following to your `.vscode/mcp.json`:

```jsonc
{
    "servers":{
         "codescribe": {
            "type": "stdio",
            "command": "uv",
            "args": ["run", 
                "--directory", 
                "${workspaceFolder}",
                "${workspaceFolder}/codescribe-agent.py",
                "mcp"
            ]
        }
    }
}
```

This configuration ensures the Python agent is started correctly as an MCP server using `uv`.

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
