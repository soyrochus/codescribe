
**Description for the Codescribe**

> Adds a free-form note, idea, reminder, or comment to the developer’s personal journal for this project (saved as a dated text file in the `.journal` folder).
>
> You can use this tool to record:
> – Work-in-progress thoughts
> – Personal reminders
> – Design decisions
> – Reflections, doubts, or open questions
> – Context about why something was done
> – TODOs or things to revisit
>
> **Trigger this tool with any natural instruction such as:**
> – “Add a note that…”
> – “Remember to…”
> – “Jot down…”
> – “Make a comment about…”
> – “Add to the project journal that…”
> – “I want to keep track of…”
>
> **Do not use this tool for adding documentation or comments inside the source code.**
> Use regular code comments (`// ...` or `/** ... */`) or documentation blocks for that purpose.
>
> This journal is for personal context, process notes, or broader observations—anything you want to keep track of during development that doesn’t belong directly in the codebase.


Create a pyton version Agent.  DO NOT USE the  node.js version in codescribe-agent.js as an exampke!. Create a fully new version based on the functional description here. Not in any way influenved by the JS function.  Call it codescribe-agent.py. Use the same paradigm, description etc. Use the openai lib instead of Langchain. 

The agent should have a tool log_note which append the note to a log in the "${workspaceFolder}/.journal" folder. The logfile should be created per day. 

Although the OpenAI reference is included, the MCP server does NOT have to include connection with openai (that is for a future extension)

Complete the README file, document both the javascript and python versions in its particulars. Do not duplicate the common parts (like the description etc)

