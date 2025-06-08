# Refactoring codescribe-agent.py

IGNORE the javascript implementation

Implement the following three refactorings

## Summarize the Day’s Journal
Implement a new tool. THis one will be using openai
Function:
“Summarize today’s journal entries.”
LLM value:
Quickly generates a short summary, highlights, or action items from the raw notes.
Use case:
End of the day, a developer or team lead wants an overview or “TL;DR” of what was logged.


Use by default the the journal of the current day, if not, you need the day (journal file name) as a parameter


## Tagging & Categorization
Implement a new tool. THis one will be using openai
Function:
“Tag/categorize my journal entries by theme (bug, idea, decision, question).”

LLM value:
Adds metadata, making it easier to search or filter later.

Use by default the journal of the current day, if not, you need the day (journal file name) as a parameter

## Reactor run_cli

change the run_cli . Change it so it will be able to run one of the three tools from the commandline, 
based on the 