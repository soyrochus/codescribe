/**  Codescribe - Copyright (c) 2025, licensed: MIT, See LICENSE for details.
Codescribe MCP Server - A personal journal tool for developers
This script allows developers to log notes, summarize journal entries, and categorize them by theme.

**/
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');
const { ChatOpenAI } = require('@langchain/openai');
const { SystemMessage, HumanMessage } = require('@langchain/core/messages');
const { McpServer } = require('@modelcontextprotocol/sdk/server/mcp.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { z } = require('zod');

const envPath = process.env.CODESCRIBE_ENV_PATH || path.join(__dirname, '.env');
dotenv.config({ path: envPath });
if (!process.env.OPENAI_API_KEY) {
  console.error('OPENAI_API_KEY missing. Add it to .env at', envPath);
  process.exit(1);
}

const DESCRIPTION = `Adds a free-form note, idea, reminder, or comment to the developer's personal journal for this project (saved as a dated text file in the '.journal' folder).

Use this tool to record:
- Work-in-progress thoughts
- Personal reminders
- Design decisions
- Reflections, doubts, or open questions
- Context about why something was done
- TODOs or things to revisit

Trigger this tool with any natural instruction such as:
- 'Add a note that...'
- 'Remember to...'
- 'Jot down...'
- 'Make a comment about...'
- 'Add to the project journal that...'

Do not use this tool for adding documentation or comments inside the source code. Use regular code comments or documentation blocks for that purpose.

This journal is for personal context, process notes, or broader observations—anything you want to keep track of during development that doesn't belong directly in the codebase.`;

const MODEL = 'gpt-4.1-mini';

function logNote(note) {
  if (!note || !note.trim()) {
    throw new Error('No note content provided');
  }
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);
  const timeStr = now.toTimeString().split(' ')[0];
  const dir = path.join(process.cwd(), '.journal');
  const file = path.join(dir, `${dateStr}.txt`);
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(file, `[${timeStr}] ${note.trim()}\n`, 'utf8');
  return `📝 Logged note to ${path.relative(process.cwd(), file)}`;
}

async function openAiCall(messages) {
  const llm = new ChatOpenAI({
    openAIApiKey: process.env.OPENAI_API_KEY,
    modelName: MODEL,
    temperature: 0,
  });
  const formatted = messages.map(m => {
    if (m.role === 'system') return new SystemMessage(m.content);
    return new HumanMessage(m.content);
  });
  const res = await llm.invoke(formatted);
  return res.content.trim();
}

async function summarizeJournal(day) {
  const dateStr = day || new Date().toISOString().slice(0, 10);
  const file = path.join(process.cwd(), '.journal', `${dateStr}.txt`);
  if (!fs.existsSync(file)) {
    throw new Error(`Journal file ${file} does not exist`);
  }
  const text = fs.readFileSync(file, 'utf8');
  const messages = [
    { role: 'system', content: 'Summarize the following journal entries.' },
    { role: 'user', content: text },
  ];
  return openAiCall(messages);
}

async function categorizeJournal(day) {
  const dateStr = day || new Date().toISOString().slice(0, 10);
  const file = path.join(process.cwd(), '.journal', `${dateStr}.txt`);
  if (!fs.existsSync(file)) {
    throw new Error(`Journal file ${file} does not exist`);
  }
  const text = fs.readFileSync(file, 'utf8');
  const messages = [
    {
      role: 'system',
      content: 'Tag or categorize each journal entry by theme such as bug, idea, decision, or question.',
    },
    { role: 'user', content: text },
  ];
  return openAiCall(messages);
}

async function runCli(args) {
  if (!args.length || args.includes('-h') || args.includes('--help')) {
    console.log('Usage:');
    console.log('  node codescribe-agent.js log <text>');
    console.log('  node codescribe-agent.js summarize [day]');
    console.log('  node codescribe-agent.js tag [day]');
    console.log('  node codescribe-agent.js mcp');
    return;
  }

  const [command, ...rest] = args;
  if (command === 'log') {
    const text = rest.join(' ').trim();
    console.log(logNote(text));
    return;
  }

  if (['summarize', 'summary'].includes(command)) {
    const day = rest[0];
    console.log(await summarizeJournal(day));
    return;
  }

  if (['tag', 'categorize', 'categorise'].includes(command)) {
    const day = rest[0];
    console.log(await categorizeJournal(day));
    return;
  }

  if (command === 'mcp') {
    await startServer();
    return;
  }

  console.error(`Unknown command: ${command}`);
  console.error('Use --help for usage.');
}

async function startServer() {
  const server = new McpServer({
    name: 'Codescribe',
    version: '1.0.0',
    description: DESCRIPTION,
  });

  server.tool(
    'logNote',
    { note: z.string() },
    async ({ note }) => ({ content: [{ type: 'text', text: logNote(note) }] })
  );

  server.tool(
    'summarizeJournal',
    { day: z.string().optional() },
    async ({ day }) => ({ content: [{ type: 'text', text: await summarizeJournal(day) }] })
  );

  server.tool(
    'categorizeJournal',
    { day: z.string().optional() },
    async ({ day }) => ({ content: [{ type: 'text', text: await categorizeJournal(day) }] })
  );

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

async function main() {
  const args = process.argv.slice(2);
  if (args[0] === 'mcp') {
    await startServer();
  } else {
    await runCli(args);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
});
