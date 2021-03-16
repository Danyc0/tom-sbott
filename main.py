import os
import json
import datetime
import urllib.request
from dotenv import load_dotenv

from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('API_KEY')
CHANNEL_IDS = [int(i) for i in os.getenv('CHANNEL_IDS').split()]
POLL_FREQ_MINS = int(os.getenv('POLL_FREQ_MINS'))

TOM_SCOTT_URL = f'https://www.googleapis.com/youtube/v3/search?key={GOOGLE_API_KEY}&channelId=UCBa659QWEk1AI4Tg--mrJ2A&part=snippet,id&type=video&maxResults=1'

bot = commands.Bot(command_prefix='~')

last_video_id = ''


def log(output_str):
    print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S: ') + output_str)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord and is in the following channels:')
    for guild in bot.guilds:
        print('  ', guild.name)


def get_video_id(search_parameters='&order=date'):
    req = urllib.request.Request(f'{TOM_SCOTT_URL}{search_parameters}')
    page = urllib.request.urlopen(req).read()

    data = json.loads(page)
    return data['items'][0]['id']['videoId']


@bot.command(name='latest', help='Responds with the latest Tom Scott video')
async def latest(context):
    video_id = get_video_id()
    result = f'Latest Tom Scott video: https://www.youtube.com/watch?v={video_id}'
    log(result)
    await context.send(result)


@tasks.loop(minutes=POLL_FREQ_MINS)
async def check_if_video():
    global last_video_id

    video_id = get_video_id()
    if video_id != last_video_id and last_video_id:
        result = f'New Tom Scott video: https://www.youtube.com/watch?v={video_id}'
        log(result)

        for channel_id in CHANNEL_IDS:
            message_channel = bot.get_channel(channel_id)
            log(f' Sent to #{message_channel.name} in {message_channel.guild}')
            await message_channel.send(result)
    else:
        log(f'No new Tom Scott video :( - Latest ID: {video_id}')
    last_video_id = video_id


@check_if_video.before_loop
async def before():
    await bot.wait_until_ready()


@bot.command(name='search', help='Searches the Tom Scott archives for a search term')
async def search(context, *term):
    term = ' '.join(term)
    safe_term = urllib.parse.quote(term, safe='')

    video_id = get_video_id(f'&q={safe_term}')
    result = f'Searched for \'{term}\' and found the Tom Scott video: https://www.youtube.com/watch?v={video_id}'
    log(result)
    await context.send(result)


check_if_video.start()
bot.run(TOKEN)

