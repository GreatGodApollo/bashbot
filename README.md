# Bashbot
Bashbot is an interesting bot made in Python that has similar command syntax to bash and the linux command line.

## Features
- Mute/Unmute
- Die Roll
- Choice
- Hidden Messages
- Hidden Mutes
- Automatic Mute Setup
- Ping
- Info
- Invite

## Technology Used
- Discord.py v0.16.12
- SQLAlchemy
- SH
- Git

## Auto-Updater
I recommend running the auto updater on a cron job, I run mine every 5 minutes. The auto updating script just runs
the commands to download the latest updates from git, as well as restarting the bot using systemctl.

**Note: The Auto-Updater will likely need modifications to work in your environment, if any such modifications are made, support will not be provided.
