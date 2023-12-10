"""
Shared services for the app
"""

# imports
from config import logger


@logger.catch
async def log_in(bot, discord) -> None:
    """
    Log & Update bot status/command tree

    Args:
        bot (_type_): Bot object
        discord (_type_): Discord object
    """

    logger.info(f"Logged in as {bot.user.name}")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(name="Creating Trade Alerts 📈"),
    )
