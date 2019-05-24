# RetBot

Discord bot built for EsfandTV Discord @ http://discord.gg/esfandtv

## Commands

### General
```
Permissions: Admin
1) !reload
2) !blacklist add/remove WORD
```
1) Force reloads the settings file used by the bot.
2) Add/Removes WORD to/from the blacklist. This is the blacklist that messages, usernames and nicknames are checked against.

### Admin
```
Permissions: Admin
1) !log blacklist add/remove
2) !log blacklist
3) !log setchannel
4) !log setchannel clear
5) !ban MEMBER PURGE (LENGTH) (REASON)
6) !purge NUMBER
7) !role reaction EMOJI_ID ROLE_ID
8) !channel mark/unmark EMOJI_ID
9) !role add/remove LEVEL_NAME ROLE_ID
10) !role print (LEVEL_NAME)

```
 1) This adds/removes the channel the command is run in to the ignore list for activity logging.
 2) Alias for !log blacklist add.
 3) This sets the channel that will hold activity logs based on the channel the commands is run in.
 4) This clears and disables activity logging.
 5) This DMs a MEMBER the ban appeal form and then subsequent bans MEMBER for REASON and purges their activity for PURGE_LENGTH days prior. Reason is optional.
 6) Deletes NUMBER previous messages
 7) Adds an EMOJI_ID ROLE_ID pairing so that if a message in a channel that is on watch gets that emoji as a reaction, if will promote that person to the given role.
 8) Marks/Unmarks a channel to be monitored for reactions using EMOJI_ID
 9) Adds/Removes an internal permission level of LEVEL_NAME that is paired to all ROLE_ID's added to it.
10) Prints all roles under LEVEL_NAME or all roles if LEVEL_NAME is not given.

### Staff

### Users
