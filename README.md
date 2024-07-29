# Discord Bot

This is a comprehensive Discord bot designed to manage user levels, roles, and moderation tasks. The bot tracks user experience (exp) and levels, assigns roles based on levels, and provides moderation commands like banning, kicking, muting, and unmuting members. Additionally, it logs member joins, leaves, message edits, deletions, and role changes.

## Features

### User Experience and Levels

- **Experience Tracking:** Users gain experience points (exp) with each message they send.
- **Leveling System:** Users are assigned levels based on their accumulated exp.
- **Role Assignment:** Users are automatically assigned roles when they reach certain levels.

### Moderation Commands

- **Ban:** Bans a user from the server.
- **Kick:** Kicks a user from the server.
- **Mute:** Mutes a user for a specified amount of time.
- **Unmute:** Unmutes a user.
- **User Info:** Displays detailed information about a user.

### Logging

- **Member Join/Leave:** Logs when members join or leave the server.
- **Message Edits/Deletions:** Logs when messages are edited or deleted.
- **Role Changes:** Logs when roles are created or deleted, and when server permissions are updated.

## Commands

### General

- `Qhello`: Greets the user.
- `Qleaderboard`: Displays the leaderboard of users based on their experience points.

### Moderation

- `Qban <member> [reason]`: Bans the specified member with an optional reason.
- `Qkick <member> [reason]`: Kicks the specified member with an optional reason.
- `Qmute <member> <timelimit> [reason]`: Mutes the specified member for the specified time limit with an optional reason. Time limit can be specified in seconds (`s`), minutes (`m`), hours (`h`), or days (`d`).
- `Qunmute <member>`: Unmutes the specified member.
- `Quser <member>`: Displays information about the specified member.

### Configuration
 `User Data `: User data is stored in user_data.json. If the file doesn't exist, it will be created automatically.
 `Level Thresholds `: Levels are determined based on the level_thresholds list.
### Events
 `on_ready `: Triggered when the bot is online.
 `on_message `: Processes user messages to update exp and levels.
 `on_member_join `: Logs when a new member joins the server.
 `on_member_remove `: Logs when a member leaves the server.
 `on_voice_state_update `: Tracks voice state updates to calculate voice time.
 `on_message_edit `: Logs when a message is edited.
 `on_message_delete `: Logs when a message is deleted.
 `on_guild_role_create `: Logs when a new role is created.
 `on_guild_role_delete `: Logs when a role is deleted.
 `on_guild_update `: Logs when server permissions are updated.
### Notes
Ensure the bot has the necessary permissions to manage roles, ban, kick, mute members, and send messages in the specified logging channels.
Modify the role names and thresholds in the assign_role function to match your server's configuration.
Logging channels (ml, msglogs, serverlogs, enterleave-logs, moderation-logs) should be created in the server to enable logging.
