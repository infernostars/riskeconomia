# Importing our custom variables/functions from backend
from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template

import discord
from discord import app_commands
from discord.ext import commands
# For time command
from datetime import datetime, timedelta
import time


class TimeCog(commands.GroupCog, group_name="time"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: time loaded")

    @app_commands.command(name="time")
    async def time(self, interaction: discord.Interaction):
        """
        Tells you the date and time in roleplay based on the current date and time in real life.
        """
        rlepoch = 1710106702.049 # As spoken and confirmed with by Mecanimetales, these correspond to the real life..
        rpepoch = -783754059.049 # ..and roleplay epochs respectively, with 91.310625 roleplay seconds passing for
        currentrl = time.time()  # every 1 second in real life. This is what the time command sets out to do.
        currentrp = rpepoch+((currentrl-rlepoch)*91.310625)
        try:
            readable = (datetime.utcfromtimestamp(0)+timedelta(seconds=currentrp)).strftime('%d %B %Y %H:%M:%S')
            embed = embed_template("The current date and time is:", readable)
            await interaction.response.send_message(embeds=[embed])
        except Exception as e:
            error_embed = error_template(f"Time command failed.\n{e}")
            logging.log.exception()
            await interaction.response.send_message(embeds=[error_embed])

# The `setup` function is required for the cog to work
async def setup(client):
    await client.add_cog(TimeCog(client))
