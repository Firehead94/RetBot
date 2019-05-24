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
5) !ban MEMBER PURGE_LENGTH REASON
6) !purge NUMBER
```
1) This adds/removes the channel the command is run in to the ignore list for activity logging.
2) Alias for !log blacklist add.
3) This sets the channel that will hold activity logs based on the channel the commands is run in.
4) This clears and disables activity logging.
5) This DMs a MEMBER the ban appeal form and then subsequent bans MEMBER for REASON and purges their activity for PURGE_LENGTH days prior. Reason is optional.
6) Deletes NUMBER previous messages

### Staff

### Users
