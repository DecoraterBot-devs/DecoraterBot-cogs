<!--
Remove any section(s) that does not apply to this pull request.
-->

### Submitting new cogs

So, you want to submit a new cog for DecoraterBot? Awesome. Now first things first, does it meet these requirements?

Does your submition:

- [ ] Have every line of code at 79 characters or less.
- [ ] Is not error prone (does not raise exceptions)
- [ ] If it experiences an Error, does it catch it and try to retry using another method (if possible) or does it allert the bot owner or server owner that the bot cannot send messages in a server / channel (if configured).
- [ ] Meets PEP8 on hangling line indents.
- [ ] Does not have hacks to avoid issues.
- [ ] Follow examples of the current existing cogs on how they are made with an all commands fed into ``self.bot.add_commands`` as a list to update the list when your cog is loaded and is removed from the list with ``self.bot.remove_commands`` with the same list when unloaded.
- [ ] Added entries for the new plugin cog to ``cogslist.json``.
- [ ] Added documentation for commands in the cog to ``Commands.md``.

### Patching or editing cogs

So, you patched a bug or optimized a cog or command? Good work. How do you meet these requirements?

Does your edit:

- [ ] Have every line of code at 79 characters or less.
- [ ] Is not error prone (does not raise exceptions)
- [ ] If it experiences an Error, does it catch it and try to retry using another method (if possible) or does it allert the bot owner or server owner that the bot cannot send messages in a server / channel (if configured).
- [ ] Meets PEP8 on hangling line indents.

<!--
And do not forget a brief description at what your new cog submission or Patched/edited cogs do here.
-->
