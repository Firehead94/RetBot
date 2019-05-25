# RetBot

Discord bot built for EsfandTV Discord @ http://discord.gg/esfandtv

## Commands

### Admin
```
1) !role reaction EMOJI_ID ROLE_ID
2) !channel mark/unmark EMOJI_ID
3) !role add/remove LEVEL_NAME ROLE_ID
4) !permissions set/remove LEVEL_NAME COMMAND_NAME
5) !log blacklist add/remove

```
1) Assigned a ROLE_ID to an EMOJI_ID that is set if a channel that is marked sees that EMOJI_ID as a reaction.
2) Marks/Unmarks a channel to watch for EMOJI_ID reactions to trigger 1).
3) Adds/Removes a role assigned to LEVEL_NAME. Multiple roles can be assigned to one LEVEL_NAME.
4) Sets/Removes COMMAND_NAME permissions from LEVEL_NAME.
5) Adds/Removes a channel to the blacklist for the activity log.

### Moderator
```
1) !permissions print LEVEL_NAME
2) !ban MEMBER PURGE [LENGTH] [REASON]
3) !blacklist add/remove WORD
4) !role print [LEVEL_NAME]
5) !purge NUMBER
```
1) Prints the commands LEVEL has access to
2) This DMs a MEMBER the ban appeal form and then subsequent bans MEMBER for REASON and purges their activity 
3) Add/Removes WORD to/from the blacklist. This is the blacklist that messages, usernames and nicknames are checked against.
4) Prints a list of LEVEL_NAMEs and the corrosponding discord roles. If a LEVEL_NAME is passed then it will only print for that 1 LEVEL_NAME.
5) Purges NUMBER of previous messages in the channel.


### Everyone
```
1) !item
2) !spell
3) !quest
```
Unavailable