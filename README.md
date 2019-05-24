# RetBot

Discord bot built for EsfandTV Discord @ http://discord.gg/esfandtv

## Commands

### Admin
```
!getRoles USER_MENTION
```
Admin Perms Required
Prints the users list of roles to the console

```
!purgeChannel NUMBER
```
Admin Perms Required
Purges the last NUMBER of messages in the channel

### Staff
```
!ban USER_MENTION PURGE_TIME REASON
```
Mod Role Required
Bans USER_MENTION and purges messages from the past PURGE_TIME days (up to 7). Attaches reason REASON to the ban. This will also DM the USER_MENTION with a link to the ban appeal form

```
!blacklist add WORD
!blacklist remove WORD
```
These commands add and remove WORD from the global blacklist. Mods are unaffected by the blacklist. Blacklist affects messages, usernames, and nick names.

```
!blacklist print
```
Print the blacklist. Only usable in the botcommands and mod-chat channels.

### Users
```
!item ITEM_NAME class=CLASS
```
Any user
Responds with an embeded message of the item. If the item has multiple types depending on class (i.e. Atiesh) then a class name can be passed. If no item is found matching that name it will respond with "no item found". If multiple items are found then a list of the top 10 results will be posted.

```
!ability ABILITY_NAME RANK
```
Any user
Responds with an embeded message of the ability. If RANK value is passed, it will attempt to get the spell ID with that rank, otherwise it will respond with the highest rank available. If no ability is found matching that name then it will respond with "no ability found". If multiple abilities are found then a list of the top 10 results will be posted.

## Logging
The server-log channel holds logs for the server. This channel logs things such as User Bans, Username Changes, Message Deletion, Bulk Message Deletion, Message Edits, User Leaves, User Joins, Nickname Changes, and User Unbans
