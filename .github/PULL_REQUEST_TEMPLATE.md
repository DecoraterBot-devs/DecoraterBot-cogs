<!--
Remove any section(s) that does not apply to this pull request.
-->

### Submitting new cogs

So, you want to submit a new cog for DecoraterBot? Awesome.

However does it meet these requirements?

- [ ] Have every line of code at 79 characters or less.
- [ ] Is not error prone (does not raise exceptions)
- [ ] If it experiences an Error, does it catch it and try to retry using another method (if possible) or does it allert the bot owner or server owner that the bot cannot send messages in a server / channel (if configured).
- [ ] Meets PEP8 on hangling line indents.
- [ ] Does it not have hacks to try to avoid issues.
- [ ] Follow examples of the current existing cogs on how they are made with an all commands fed into ``self.bot.add_commands`` as a list to update the list when your cog is loaded and is removed from the list with ``self.bot.remove_commands`` with the same list when unloaded.
- [ ] Added entries for the new plugin cog to ``cogslist.json``.
- [ ] Added documentation for commands in the cog to ``Commands.md``.

### Patching or editing cogs

So, you patched a bug or optimized a cog or command? Good work. How do you meet these requirements?

However does it meet these requirements?

- [ ] Have every line of code at 79 characters or less.
- [ ] Is not error prone (does not raise exceptions)
- [ ] If it experiences an Error, does it catch it and try to retry using another method (if possible) or does it allert the bot owner or server owner that the bot cannot send messages in a server / channel (if configured).
- [ ] Meets PEP8 on hangling line indents.

<!--
The following is not needed when submitting new cogs. However you still have to Document any new command added from the cog(s).
-->
### Patching or fixing Command Documentation

So, you patched an existing Command's Documentation or Added Documentation to a command that was forgotten in the Documentation? Excelent.

However does it meet these requirements?

- [ ] Does it provide an description of the command and the command name with how to invoke it (if the command takes arguments).
- [ ] Does it separate commands per cog file (so it can help stop confusion when bot says the command does not exist).

<!--
And do not forget a brief description on what your changes/submissions do here.
-->
