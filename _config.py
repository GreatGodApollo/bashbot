class Config:
    token = "Your token here"  # Retrieved from Discord Developer's portal
    description = "A cool bot that acts like bash"  # Generic description of what your bot does
    owners = ["YourID"]  # Your Discord user ID
    prefixes = ["./"]  # Bot prefix
    cogs = ["cogs.owner", "cogs.apt", "cogs.misc", "cogs.administration", "cogs.moderation", "cogs.config",
            "cogs.hidden", "cogs.repl", "cogs.random"]  # List of cogs bot should initially load
    dburl = "DB Connection URL"  # Crafted using the sqlalchemy docs
    workingDirectory = "/your/working/directory/"  # Trailing slash is important!
    serviceName = "yourServiceName"  # Systemctl service name
