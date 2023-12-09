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
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Routing Tradingview Alerts",
        ),
    )
    await bot.tree.sync()
