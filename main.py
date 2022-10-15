import os
import re
import json
import datetime
import requests
import urllib.request
from dotenv import load_dotenv

from discord.ext import commands, tasks
from discord import Intents

from quart import Quart
from quart import request

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('API_KEY')
CHANNEL_IDS = [int(i) for i in os.getenv('CHANNEL_IDS').split()]
CALLBACK_URL = os.getenv('CALLBACK_URL')
RESUBSCRIBE_DAYS = int(os.getenv('RESUBSCRIBE_DAYS'))
TOM_SCOTT_ID = 'UCBa659QWEk1AI4Tg--mrJ2A'
TOM_SCOTT_URL = f'https://www.googleapis.com/youtube/v3/search?key={GOOGLE_API_KEY}&channelId={TOM_SCOTT_ID}&part=snippet,id&type=video&maxResults=1'

#app = Flask(__name__)
intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='~', intents=intents)
app = Quart(__name__)

message_channels = []
last_video_id = ''

def log(output_str):
    print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S: ') + output_str)


@bot.event
async def on_ready():
    if message_channels:
        log('on_ready() called but channels already added. Skipping adding channels')
    else:
        for channel_id in CHANNEL_IDS:
            channel = bot.get_channel(channel_id)
            if channel:
                message_channels.append(channel)
            else:
                log(f' Failed to access channel with ID: {channel_id}')
    resubscribe.start()
    bot.loop.create_task(app.run_task('0.0.0.0', 5000))

    print(f'{bot.user.name} has connected to Discord and is in the following servers:')
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


@bot.command(name='search', help='Searches the Tom Scott archives for a search term')
async def search(context, *term):
    term = ' '.join(term)
    safe_term = urllib.parse.quote(term, safe='')

    video_id = get_video_id(f'&q={safe_term}')
    result = f'Searched for \'{term}\' and found the Tom Scott video: https://www.youtube.com/watch?v={video_id}'
    log(result)
    await context.send(result)


@app.route('/feed', methods=['GET', 'POST'])
async def feed():
    global last_video_id
    challenge = request.args.get('hub.challenge')
    if (challenge):
        log('Received a challenge request')
        return challenge

    raw_response = await request.data
    response = raw_response.decode('utf-8')
    video_id = re.search('<yt:videoId>(.+)</yt:videoId>', response).group(1)
    if video_id == last_video_id:
        log(f'Repeated notification for video https://www.youtube.com/watch?v={video_id} - It\'s probably an edit so I won\'t post it')
    else:
        last_video_id = video_id
        result = f'Latest Tom Scott video: https://www.youtube.com/watch?v={video_id}'

        log(result)

        for message_channel in message_channels:
            log(f' Sent to #{message_channel.name} in {message_channel.guild}')
            await message_channel.send(result)

    return '', 204


@tasks.loop(hours=RESUBSCRIBE_DAYS * 24)
async def resubscribe():
    url = 'https://pubsubhubbub.appspot.com/subscribe'
    lease_length = int(RESUBSCRIBE_DAYS * 24 * 60 * 60) + 20
    myobj = {'hub.callback': CALLBACK_URL, 'hub.topic': f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={TOM_SCOTT_ID}', 'hub.verify': 'Asynchronous', 'hub.mode': 'Subscribe', 'hub.lease_seconds': lease_length}

    requests.post(url, data = myobj)
    log('Resubscribed to the hook')


@resubscribe.before_loop
async def before():
    await bot.wait_until_ready()


bot.run(TOKEN)

