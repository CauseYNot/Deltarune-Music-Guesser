
import os
import random

from discord import Embed, FFmpegPCMAudio, VoiceChannel
from discord.commands import option
from discord.ext import bridge
from discord.ext.pages import Page, Paginator
from discord.utils import basic_autocomplete
from dotenv import load_dotenv
from tabulate import tabulate

from ost_choices import soundtrack_choices

# Load .env
load_dotenv()
# Set constants and bot
TOKEN = os.getenv('TOKEN')
bot = bridge.Bot()
music_files = os.listdir('./audio')
music_files.remove('.DS_Store')

total_rounds = 0
rounds_to_play = 0
current_song = None
player_usernames = []
player_ids = []
players_to_guess = []
guesses = {}
scores = {}

def pages_for_scores(guesses, scores, rounds):
    overview_embed = Embed(
        title='Scores',
        description='\n'.join([f'{player}: {scores[player]}/{rounds}' for player in scores]),
        colour=0xffffff
        )
    overview_embed.set_footer(text='Next page for detailed info')
    overview_page = Page(embeds=[overview_embed])
    detailed_embed = Embed(
        title='Guesses',
        description='```' + tabulate(guesses, headers=['Q:'] + player_usernames + ['Song name']) + '```',
        colour=0xffffff
    )
    detailed_page = Page(embeds=[detailed_embed])
    return [overview_page, detailed_page]

@bot.slash_command(name='start_quiz', description='Bind the bot to a voice channel and start a music quiz')
@option('channel', type=VoiceChannel, description='The voice channel to bind the bot to - (all users in the voice channel will play the quiz)', required=True)
@option('rounds', type=int, description='The number of rounds to play', choices=list(range(1, 21)), required=True)
async def start_quiz(ctx, channel, rounds):
    global total_rounds
    global rounds_to_play
    global current_song
    global player_usernames
    global player_ids
    global players_to_guess
    global guesses
    
    if current_song:
        await ctx.respond(embed=Embed(title='A quiz is already in progress!', colour=0xff0000))
        return
    
    player_ids = list(channel.voice_states.keys())
    if player_ids == []:
        await ctx.respond(embed=Embed(title='There are no users in the voice channel', colour=0xff0000))
        return
    
    guesses = {
        'Q': list(range(1, rounds + 1))
    }
    for player_id in player_ids:
        guesses[f'<@!{player_id}>'] = []
        scores[f'<@!{player_id}>'] = 0
    
    guesses['Song name'] = []
    player_usernames = [(await bot.fetch_user(id)).display_name for id in player_ids]
    players_to_guess = player_ids.copy()
    # Bind to a voice channel
    await channel.connect()
    await ctx.respond(embed=Embed(title=f'Bot bound to `{channel.name}`!', colour=0xffffff))
    await ctx.send(embed=Embed(title='Starting quiz!', description='Players are:\n- <@!{}>'.format(">\n- <@!".join(map(str, player_ids))), colour=0xffffff))
    total_rounds = rounds
    rounds_to_play = rounds
    await ctx.send(embed=Embed(title=f'Starting round! {rounds_to_play} rounds left', colour=0xffffff))
    current_song = random.choice(music_files)
    guesses['Song name'].append(current_song[:-4])
    ctx.voice_client.play(source=FFmpegPCMAudio('./audio/' + current_song, executable='./ffmpeg'))

@bot.slash_command(name='guess', description='Guess the song')
@option('guess', type=str, description='The guess (type for more options)', required=True, autocomplete=basic_autocomplete(soundtrack_choices))
async def guess(ctx, guess):
    global current_song
    global rounds_to_play
    global players_to_guess
    global guesses
    global scores
    if ctx.author.id not in players_to_guess:
        await ctx.send(embed=Embed(title=f'You are not part of this quiz. Please try later', colour=0xff0000))
        return
    
    players_to_guess.remove(ctx.author.id)
    
    if f'{guess}.mp3' == current_song[5:]:
        guesses[f'<@!{ctx.author.id}>'].append('✅')
        scores[f'<@!{ctx.author.id}>'] += 1
        await ctx.respond(embed=Embed(
            title='Correct!', colour=0x00ff00
            ))
    else:
        guesses[f'<@!{ctx.author.id}>'].append('❌')
        await ctx.respond(embed=Embed(
            title='Incorrect!', colour=0xff0000
            ))
        
    if len(players_to_guess) == 0:
        await ctx.send(embed=Embed(title=f'Round finished! The audio was {current_song[:-4]}', colour=0x00ff00))
        current_song = None
        rounds_to_play -= 1
        players_to_guess = player_ids.copy()
        if rounds_to_play == 0:
            await ctx.send(embed=Embed(title='Quiz finished!', colour=0xffffff))
            await Paginator(pages=pages_for_scores(guesses, scores, total_rounds)).respond(ctx)
            guesses, scores = {}, {}
            await ctx.voice_client.disconnect()
        else:
            await ctx.send(embed=Embed(title=f'Starting round! {rounds_to_play} rounds left', colour=0xffffff))
            ctx.voice_client.stop()
            current_song = random.choice(music_files)
            guesses['Song name'].append(current_song[:-4])
            ctx.voice_client.play(source=FFmpegPCMAudio('./audio/' + current_song, executable='./ffmpeg'))
    else:
        await ctx.send(embed=Embed(title=f'{len(players_to_guess)} answers left', colour=0xffffff))
        

bot.run(TOKEN)