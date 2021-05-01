# Tom SBott
A simple (unofficial) Discord bot for announcing when Tom Scott posts a new YouTube video

## Dependencies
    pip install -U Discord.py python-dotenv

## Setup

You'll need to create a discord bot of your own in the [Discord Developer Portal](https://discord.com/developers/applications) with View Channels and Read Messages permissions. It's also handy if you have an empty server (or "guild") for you to test in. This section of [this guide](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal) may be helpful to set that up.

You'll need to set four environment variables:
* DISCORD_TOKEN -> The Discord token for the bot you created (Available on your bot page in the developer portal)
* API_KEY -> Your Google API key so the bot can query the YouTube API
* CHANNEL_IDS -> A space-separated list of the channel IDs in which to post the latest video link
* RESUBSCRIBE_DAYS -> The number of days between resubscriptions to the YouTube API Push Notifications (4 seems to be a good value for this)
* CALLBACK_URL -> The URL that the YouTube API Push Notifications are sent to

You can put these in a .env file in the repo directory as it uses dotenv (See [here](https://pypi.org/project/python-dotenv/) for usage) so you don't have to keep them in your environment

## Contributions

In short, patches welcome. If you raise a PR, I'll test it and (probably) merge it
