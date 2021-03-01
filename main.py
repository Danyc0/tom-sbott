import os
import json
import urllib.request
from dotenv import load_dotenv

from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('API_KEY')
CHANNEL_IDS = [int(i) for i in os.getenv('CHANNEL_ID').split()]

TOM_SCOTT_URL = f'https://www.googleapis.com/youtube/v3/search?key={GOOGLE_API_KEY}&channelId=UCBa659QWEk1AI4Tg--mrJ2A&part=snippet,id&order=date&maxResults=1'


bot = commands.Bot(command_prefix='~')

last_video_id = ''


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord and is in the following channels:')
    for guild in bot.guilds:
        print('  ', guild.name)

def get_latest_id():
    req = urllib.request.Request(TOM_SCOTT_URL)
    page = urllib.request.urlopen(req).read()

    data = json.loads(page)
    return data['items'][0]['id']['videoId']

@bot.command(name='latest', help='Responds with the latest Tom Scott video')
async def latest(context):
    print('Latest video requested')
    
    video_id = get_latest_id()
    result = f'Latest Tom Scott video: https://www.youtube.com/watch?v={video_id}'
    print(result)
    await context.send(result)


@tasks.loop(hours=1)
async def check_if_video():
    global last_video_id

    video_id = get_latest_id()
    if video_id != last_video_id and last_video_id:
        last_video_id = video_id

        result = f'New Tom Scott video: https://www.youtube.com/watch?v={video_id}'
        print(result)

        for channel_id in CHANNEL_IDS:
            message_channel = bot.get_channel(channel_id)
            print(f' Sent to #{message_channel.name} in {message_channel.guild}')
            await message_channel.send(result)
    else:
        print('No new Tom Scott video :(')


@check_if_video.before_loop
async def before():
    await bot.wait_until_ready()


@bot.event
async def on_reaction_add(reaction, user):
    print(reaction, user)
    await reaction.remove(user)


check_if_video.start()
bot.run(TOKEN)

