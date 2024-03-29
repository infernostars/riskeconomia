# Importing our custom variables/functions from backend
from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import time

# Don't mind these universal constants, putting them here because I don't want numerous copies of these in the code.
rlepoch = 1710106702.049 # As spoken and confirmed with by Mecanimetales, these correspond to the real life and
rpepoch = -783754059.049 # roleplay epochs respectively, with 91.310625 roleplay seconds passing for every second IRL.

class TimeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: time loaded")

    @app_commands.command(name="current")
    async def current(self, interaction: discord.Interaction):
        """
        Tells you the date and time in roleplay based on the current date and time in real life.
        """
        currentrl = time.time() 
        currentrp = rpepoch+((currentrl-rlepoch)*91.310625)
        try:
            readable = (datetime.utcfromtimestamp(0)+timedelta(seconds=currentrp)).strftime('%d %B %Y %H:%M:%S')
            embed = embed_template("The current date and time is:", readable)
            await interaction.response.send_message(embeds=[embed])
        except Exception as e:
            error_embed = error_template(f"Current command in time cog failed.\n{e}")
            logging.log.exception()
            await interaction.response.send_message(embeds=[error_embed])
    
    @app_commands.command(name="whenis")
    @app_commands.choices(modes=[
        app_commands.Choice(name="Roleplay", value="rp"),
        app_commands.Choice(name="Real Life", value="rl")
        ])
    async def whenis(self, interaction: discord.Interaction, modes: app_commands.Choice[str], timestamp: float,):
        """
        Gives you both roleplay and real life time based on the unix timestamp given.
        """
        if modes.value == "rp":
            rptime = rpepoch+((timestamp-rlepoch)*91.310625)
            try:
                rlreadable = (datetime.utcfromtimestamp(0)+timedelta(seconds=timestamp)).strftime('%d %B %Y %H:%M:%S')
                rpreadable = (datetime.utcfromtimestamp(0)+timedelta(seconds=rptime)).strftime('%d %B %Y %H:%M:%S')
                embed = embed_template(f"Assuming the input given is {rlreadable}:", rpreadable)
                await interaction.response.send_message(embeds=[embed])
            except Exception as e:
                error_embed = error_template(f"Whenis Roleplay command in time cog failed.\n{e}")
                logging.log.exception()
                await interaction.response.send_message(embeds=[error_embed])
        elif modes.value == "rl":
            rltime = rlepoch+((timestamp-rpepoch)*91.310625)
            try:
                rlreadable = (datetime.utcfromtimestamp(0)+timedelta(seconds=rltime)).strftime('%d %B %Y %H:%M:%S')
                rpreadable = (datetime.utcfromtimestamp(0)+timedelta(seconds=timestamp)).strftime('%d %B %Y %H:%M:%S')
                embed = embed_template(f"Assuming the input given is {rpreadable}:", rlreadable)
                await interaction.response.send_message(embeds=[embed])
            except Exception as e:
                error_embed = error_template(f"Whenis Real Life command in time cog failed.\n{e}")
                logging.log.exception()
                await interaction.response.send_message(embeds=[error_embed])
        else:
            error_embed = error_template(f"..what the fuck? How?! Contact LegitSi immediately!\n{e}")
            logging.log.exception()
            await interaction.response.send_message(embeds=[error_embed])

# The `setup` function is required for the cog to work
async def setup(client):
    await client.add_cog(TimeCog(client))
