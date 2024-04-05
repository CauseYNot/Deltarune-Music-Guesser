
import json
import os

import discord
from discord.commands import option
from discord.ext import bridge
from dotenv import load_dotenv

# Load .env
load_dotenv()
# Set constants and bot
TOKEN = os.getenv('TOKEN')
bot = bridge.Bot()

currently_playing = False

@bot.slash_command(name='bind', description='Bind the bot to a voice channel')
async def bind(ctx, channel: discord.VoiceChannel):
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.respond(discord.Embed(title=f'Bot bound to `{channel.name}`!', colour=0xffffff))
        return
    
    await channel.connect()
    await ctx.respond(embed=discord.Embed(title=f'Bot bound to `{channel.name}`!', colour=0xffffff))


bot.run(TOKEN)
