Understood. You want a **tool description** that:

* Clearly signals *what* goes into the journal vs. code documentation.
* Allows a variety of natural triggers (“add a note,” “write a comment,” “jot this down,” “remember…” etc.), not a fixed phrase.
* Steers away from direct code documentation.

Here’s a refined, flexible description for the tool—without assuming any fixed invocation phrase:

---

**Description for the Journal Tool**

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

---

This makes the distinction explicit, invites a variety of phrasing, and is natural to read—while blocking misuse for in-code documentation. If you want it even more concise or with more examples, just say so.
