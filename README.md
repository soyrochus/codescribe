# CodeScribe

CodeScribe is a journaling agent that lets you log coding notes using natural language. It uses LangChain.js, the Model Context Protocol (MCP) SDK and OpenAI to interpret your instructions and write them to daily journal files.

## Install

```bash
npm install
```


## Run

Start the MCP server. It listens on stdin/stdout so it can be invoked by any MCP-compliant host:

```bash
node codescribe-agent.js
```
The notes are stored in a `.journal` folder relative to where you run the agent. Each entry is timestamped in the form `[HH:MM:SS] message`.

Once running, send an MCP `callTool` request with your instruction. The agent logs the note in `.journal/YYYY-MM-DD.txt` and returns a confirmation message.

## MCP Server Configuration (Development Mode)

To use CodeScribe as an MCP server in development mode within this project, add the following configuration to your `.vscode/mcp.json` file:

```json
{
    "servers":{
        "codescribe": {
            "type": "stdio",
            "command": "node",
            "args": ["./codescribe-agent.js"]
        }
    }
}
```

This configuration ensures that the MCP server can find and execute `codescribe-agent.js` correctly when started from the project root.

This tells your MCP-compatible tools (such as VS Code extensions) how to launch the CodeScribe agent locally using Node.js. The agent will communicate over standard input/output and log notes as described above.

Make sure the `.vscode/mcp.json` file is located in the root of your project (inside the `.vscode` folder).

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