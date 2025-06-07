const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');
const { ChatOpenAI } = require('@langchain/openai');
const { initializeAgentExecutorWithOptions } = require('langchain/agents');
const { Tool } = require('@langchain/core/tools');
const { McpServer } = require('@modelcontextprotocol/sdk/server/mcp.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { z } = require('zod');

dotenv.config();
if (!process.env.OPENAI_API_KEY) {
  console.error('OPENAI_API_KEY missing. Add it to .env');
  process.exit(1);
}

/**
 * Journaling tool that logs developer notes into a daily file.
 * Each invocation appends the note to `.journal/YYYY-MM-DD.txt` with a timestamp.
 */
class JournalTool extends Tool {
  constructor() {
    super();
    this.name = 'journal';
    this.description = `
      Log a developer's note into today's journal file inside the '.journal' folder.
      Use this tool when the user says things like:
      "note that...", "write down...", "add annotation...", or "make a note..."
      Input should be the full note content.
    `;
  }

  /**
   * Append the given note to today's journal file.
   * @param {string} note - The note text to log.
   * @returns {string} Confirmation message with the file path.
   */
  async _call(note) {
    if (!note || !note.trim()) {
      throw new Error('No note content provided');
    }
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10); // YYYY-MM-DD
    const timeStr = now.toTimeString().split(' ')[0]; // HH:MM:SS
    const dir = path.join(process.cwd(), '.journal');
    const file = path.join(dir, `${dateStr}.txt`);
    const line = `[${timeStr}] ${note.trim()}\n`;
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(file, line, 'utf8');
    return `📝 Logged note to ${path.relative(process.cwd(), file)}`;
  }
}

// Helper to build a LangChain agent with the journaling tool
async function createExecutor() {
  const llm = new ChatOpenAI({
    openAIApiKey: process.env.OPENAI_API_KEY,
    modelName: 'gpt-3.5-turbo',
    temperature: 0,
  });
  const tools = [new JournalTool()];
  return initializeAgentExecutorWithOptions(tools, llm, {
    agentType: 'openai-functions',
    verbose: false,
  });
}

// CLI mode: log a note directly
async function runCli(input) {
  const executor = await createExecutor();
  const result = await executor.run(input);
  console.log(result);
}

// Start an MCP server exposing a tool that routes input through the agent
async function startServer() {
  const server = new McpServer({
    name: 'CodeScribe',
    version: '1.0.0'
  });

  server.tool(
    'logNote',
    { input: z.string() },
    async ({ input }) => {
      const executor = await createExecutor();
      const result = await executor.run(input);
      return { content: [{ type: 'text', text: result }] };
    }
  );

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// Decide mode based on command line arguments
const userInput = process.argv.slice(2).join(' ').trim();
if (userInput) {
  runCli(userInput).catch(err => {
    console.error('Error:', err.message);
  });
} else {
  startServer().catch(err => {
    console.error('Server error:', err.message);
  });
}
