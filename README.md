# CodeScribe

CodeScribe is a journaling agent that lets you log coding notes using natural language. It uses LangChain.js, the Model Context Protocol (MCP) SDK and OpenAI to interpret your instructions and write them to daily journal files.

## Install

```bash
npm install
```

Create a `.env` file with your OpenAI API key so the agent can reach the OpenAI API:

```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

## Run

Start the MCP server. It listens on stdin/stdout so it can be invoked by any MCP-compliant host:

```bash
node codescribe-agent.js
```
The notes are stored in a `.journal` folder relative to where you run the agent. Each entry is timestamped in the form `[HH:MM:SS] message`.

Once running, send an MCP `callTool` request with your instruction. The agent logs the note in `.journal/YYYY-MM-DD.txt` and returns a confirmation message.
