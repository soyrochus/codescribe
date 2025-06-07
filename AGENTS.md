## 🧠 Prompt: **Implement a Real Coding Agent with Journaling Tool (CodeScribe)**

You are a senior AI engineer developing a real, functioning AI coding assistant component, not a mock or demo. You must implement a journaling agent in **JavaScript (Node.js)** using **LangChain.js**, exposing a **Model-Context-Protocol (MCP)**-compliant interface. Your agent will be called "CodeScribe" and will allow developers to **log contextual notes** directly from their IDE (e.g., through GitHub Copilot or another MCP-compliant host).

---

### 🎯 Objective

Build a **working agent** named `CodeScribe` that can:

* Accept **natural language instructions** like:

  * *"Write down: Fix login timeout bug tomorrow."*
  * *"Note: check if regex is needed for email validation."*
* Use an **LLM** (OpenAI GPT-3.5 or GPT-4) to interpret intent.
* Invoke a **custom journaling tool**, which:

  * Saves the message into a text file in `.journal/YYYY-MM-DD.txt`.
  * Includes a timestamp for each entry.
* Follow the **MCP architecture**, where:

  * The LLM is the *Model*.
  * The user's input and available tools form the *Context*.
  * The journaling server/tool is an *external Protocol endpoint* or local callable tool.

---

### 📦 Requirements

* Use **LangChain.js** to implement the LLM and agent infrastructure.
* Use only **basic JavaScript**, no TypeScript.
* The agent must be **functional end-to-end**: input > LLM > tool > result.
* Include detailed **documentation** in comments.
* Use **Node.js file system (fs)** API for file writes.
* Input must be flexible (not just `"Journal:"`) – accept `"Note:"`, `"Write down:"`, `"Remember to..."`, `"Add an annotation:"`, etc.
* Output should clearly confirm the logging was successful.

---

### 🧰 Tech Stack

* JavaScript (Node.js)
* [LangChain.js](https://js.langchain.com/)
* [OpenAI API](https://platform.openai.com/)
* Node `fs`, `path`, and `dotenv` modules

---

### 🧪 Example Interaction

```javascript
> User: "Write down: Refactor payment processing to use async queues."
> Agent: "📝 Logged note to .journal/2025-06-07.txt"
```

---

### ✅ Deliverable

A single JavaScript file named `codescribe-agent.js` that:

1. Loads environment config (OpenAI API key).
2. Defines a journaling tool with LangChain's Tool class.
3. Instantiates an OpenAI model via LangChain.
4. Configures an agent that:

   * Parses user input.
   * Determines whether to invoke the journaling tool.
   * Writes to the file if needed.
   * Returns confirmation.
5. Handles errors gracefully (e.g., journal folder missing, no input).
6. Includes comments explaining each part.
7. **Must run without modification** once dependencies are installed.

---

### 💡 Sample Tool Description

```js
this.description = `
  Log a developer's note into today's journal file inside the '.journal' folder.
  Use this tool when the user says things like:
  "note that...", "write down...", "add annotation...", or "make a note..."
  Input should be the full note content.
`;
```

---

### 🧪 Usage Instructions

```bash
# Install dependencies
npm install langchain @langchain/openai dotenv

# Set your OpenAI key in a .env file
echo "OPENAI_API_KEY=sk-..." > .env

# Run the agent
node codescribe-agent.js
```

---

### 📝 Sample Run Output

```bash
User: Add a note: The logging mechanism breaks on large files.
Agent: 📝 Logged note to 2025-06-07.txt
File .journal/2025-06-07.txt:
[14:32:19] The logging mechanism breaks on large files.
```

---

### 🧠 Bonus Challenge (optional)

Add support for:

* Multiple tools (e.g., a TODO tracker, calendar event tool).
* Tagging notes with context labels: "bug", "idea", "todo", etc.
* Pretty console output with colors (e.g., using `chalk`).

---
