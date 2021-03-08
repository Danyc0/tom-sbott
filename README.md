# Tom SBott
A simple (unofficial) Discord bot for announcing when Tom Scott posts a new YouTube video

## Dependencies
    pip install -U Discord.py python-dotenv

## Setup

You'll need to create a discord bot of your own in the [Discord Developer Portal](https://discord.com/developers/applications) with View Channels and Read Messages permissions. It's also handy if you have an empty server (or "guild") for you to test in. This section of [this guide](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal) may be helpful to set that up.

You'll need to set three environment variables:
* DISCORD_TOKEN -> The Discord token for the bot you created (Available on your bot page in the developer portal)
* API_KEY -> Your Google API key so the bot can query the YouTube API
* CHANNEL_IDS -> A space-separated list of the channel IDs in which to post the latest video link
* POLL_FREQ_MINS -> The number of minutes between every poll of YouTube

You can put these in a .env file in the repo directory as it uses dotenv (See [here](https://pypi.org/project/python-dotenv/) for usage) so you don't have to keep them in your environment

## Contributions

In short, patches welcome. If you raise a PR, I'll test it and (probably) merge it
