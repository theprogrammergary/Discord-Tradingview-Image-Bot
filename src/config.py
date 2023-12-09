"""
Loads environment vars from .env file
"""

# imports
import os

from dotenv import load_dotenv
from loguru import logger

# environment vars
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".setup", ".env"))
BOT_TOKEN: str | None = os.getenv(key="BOT_TOKEN")


# logger
logger.remove()
logger.add(
    sink="./logs/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    backtrace=True,
    format=(
        "\n{time:YYYY-MM-DD HH:mm:ss} {level.icon} {level} \n"
        '{file}>"{function}">{line} \n    {message} \n'
    ),
)
