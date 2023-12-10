"""
Entry for Discord Bot that acts as a controller for bot events and commands.
"""

# imports
import sys

import discord
from discord.ext import commands

import config
import services.alerts.functions as alerts
import services.shared.functions as shared
from config import logger

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    """
    Controller for on_ready event.
    """

    await shared.log_in(bot=bot, discord=discord)


@bot.event
async def on_message(message) -> None:
    """
    Controller for on_message event.
    """
    await alerts.valid_webhook_msg(message=message)
    return


@bot.event
async def on_command_error() -> None:
    """
    Controller for on_command_error event.
    """
    return


if __name__ == "__main__":
    if config.BOT_TOKEN is None:
        logger.critical("BOT_TOKEN is not configured.")
        sys.exit(1)

    bot.run(token=config.BOT_TOKEN)
