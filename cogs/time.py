# Importing our custom variables/functions from backend
from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template
from backend.utils.database import userdb, create_new_user

import discord
from discord import app_commands
from discord.ext import commands
# For time command
from datetime import datetime
from time

from tinydb import Query


class TimeCog(commands.GroupCog, group_name="time"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: time loaded")

    @app_commands.command(name="time")
    async def time(self, interaction: discord.Interaction):
        """
        Tells you the date and time in roleplay based on the current date and time in real life.
        """
      rlepoch = 1710106702.049
      rpepoch = -783754059.049
      currentrl = time.time()
      currentrp = rpepoch+((currentrl-rlepoch)*91.310625)
      if datetime.utcfromtimestamp().strftime('%-d %B %Y %H:%M:%S'):
          readable = datetime.utcfromtimestamp().strftime('%-d %B %Y %H:%M:%S')
          embed = embed_template("The current date and time is:", readable)
          await interaction.response.send_message(embeds=[embed])
      except:
          error_embed = error_template("Conversion to readable time failed. Contact LegitSi.")
          await interaction.response.send_message(embeds=[error_embed])

# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog (Example) to the name of your class.
async def setup(client):
    # Here, `Example` is the name of the class
    await client.add_cog(TimeCog(client))
