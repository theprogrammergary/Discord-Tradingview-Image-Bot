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
ALERT_CHANNEL: str | None = os.getenv(key="ALERT_CHANNEL_NAME")
ALERT_RECEIVER_NAME: str | None = os.getenv(key="ALERT_RECEVIER_NAME")
ALERT_RECEIVER: str | None = os.getenv(key="ALERT_RECEVIER")
WICK_TEST_BOT: str | None = os.getenv(key="WICK_TEST_BOT")
WICK_TEST_CHART_URL: str | None = os.getenv(key="WICK_TEST_CHART_URL")
TV_CHART: str | None = os.getenv(key="TV_CHART_URL")
REF: str | None = os.getenv(key="REF_CODE")


# global vars
FOOTER_ICON: str = (
    "https://cdn.discordapp.com/emojis/918614915563016252.webp?size=60&quality=lossless"
)
TRADING_IMAGE_URL: str = "https://s3.tradingview.com/snapshots"


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
