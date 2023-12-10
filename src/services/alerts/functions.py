"""
Service functions for turning a webhook message into a embed trade alert with image
"""


# imports
import datetime
import json

import requests

import config
from config import logger
from services.alerts import capture


# entry functions
@logger.catch
async def valid_webhook_msg(message) -> None:
    """
    Validates message is in the correct channel and then routes it
    to the appropriate alert manager

    Args:
        bot (_type_): Discord bot object
        discord (_type_): Discord object
        message (_type_): Posted message
    """

    if not message.author.bot:
        return

    if message.author.name != config.ALERT_RECEIVER_NAME:
        return

    if message.channel.name != config.ALERT_CHANNEL:
        return

    json_message = json.loads(s=str.replace(message.content, "^", '"'))

    if json_message["bot"] == "wick test":
        await wick_test_bot(alert_info=json_message)

    return


# alert routes
async def wick_test_bot(alert_info: dict) -> None:
    """
    Creates a trading alert for wick test signals

    Args:
        alert_info (json): Alert information
    """

    if config.WICK_TEST_BOT is None:
        return

    logger.info(f"NEW WICK TEST ALERT: {alert_info}")

    alert_info["base_url"] = config.WICK_TEST_CHART_URL

    await create_alert_urls(alert_info=alert_info)

    alert_message: str = create_alert_message(alert_info=alert_info)

    print(f"\n\nALERT MESSAGE: {alert_message}")

    post_alert(alert_message=alert_message, alert_url=config.WICK_TEST_BOT)

    return


# functions
def post_alert(alert_message: str, alert_url: str) -> None:
    """
    POSTs the final alert message to the

    Args:
        alert_message (str): Message in string json format
        alert_url (str): Request URL
    """

    headers: dict[str, str] = {"Content-Type": "application/json"}
    try:
        requests.post(url=alert_url, headers=headers, data=alert_message, timeout=10000)

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        logger.error(f"Alert Message: {alert_message}")


def create_alert_message(alert_info: dict) -> str:
    """
    Transform the alert info into a string (discord embed message)

    Args:
        alert_info (dict): Raw alert information

    Returns:
        str: Discord embed message fields
    """

    title_prefix: str = f'🔔 {str(object=alert_info["timeframe"])} - '
    bull_title: str = f'{title_prefix} Bull {str(object=alert_info["bot"]).title()}'
    bear_title: str = f'{title_prefix} Bear {str(object=alert_info["bot"]).title()}'
    bull_color: str = "1350948"
    bear_color: str = "14291730"

    title: str = bull_title if alert_info["type"] == 1 else bear_title
    embed_color: str = bull_color if alert_info["type"] == 1 else bear_color
    current_timestamp: str = datetime.datetime.now(datetime.timezone.utc).isoformat()

    fields: list[dict[str, str | bool]] = [
        {
            "name": "__Symbol__",
            "value": f'{str(object=alert_info["symbol"])}',
            "inline": False,
        },
        {
            "name": "__Entry__",
            "value": str(object=alert_info["entry"]),
            "inline": True,
        },
        {
            "name": "__Target__",
            "value": str(object=alert_info["target"]),
            "inline": True,
        },
        {
            "name": "__Stop__",
            "value": str(object=alert_info["stop"]),
            "inline": True,
        },
    ]

    alert_message: dict = {
        "embeds": [
            {
                "title": title,
                "fields": fields,
                "color": embed_color,
                "url": f'{alert_info["chart_url"]}',
                "image": {"url": alert_info["image_url"]},
                "footer": {
                    "text": "Powered by GG Alerts",
                    "icon_url": config.FOOTER_ICON,
                },
                "timestamp": current_timestamp,
            }
        ],
    }

    alert_message_json: str = json.dumps(obj=alert_message)

    return alert_message_json


async def create_alert_urls(alert_info: dict) -> dict[str, str]:
    """
    Driver function to create chart url and chart image url

    Args:
        alert_info (dict): Raw alert info

    Returns:
        dict[str, str]: Update alert info dict
    """

    create_image_url: str = ""
    image_url: str = ""
    # chart_url: str = ""

    # if alert_info.get("base_url"):
    #     create_image_url = tradingview_create_image_url(alert_info=alert_info)
    #     image_url, chart_url = await create_tradingview_image(
    #         create_image_url=create_image_url
    #     )

    alert_info["create_image_url"] = create_image_url
    alert_info["image_url"] = image_url
    alert_info["chart_url"] = create_image_url

    return alert_info


def tradingview_create_image_url(alert_info: dict) -> str:
    """Constructs a tradingview chart url from alert_info

    Args:
        alert_info (dict): Raw alert information

    Returns:
        str: Tradingview chart URL
    """

    chart_symbol: str = alert_info["symbol"]
    chart_interval: str = alert_info["timeframe"]
    chart_image_url: str = (
        f'{alert_info["base_url"]}theme=dark'
        f"&symbol={chart_symbol}"
        f"&interval={chart_interval}"
        f"&{config.REF}"
    )

    return chart_image_url


async def create_tradingview_image(create_image_url: str) -> tuple[str, str]:
    """
    Driver for selenium automation and cleans the urls from the automation

    Returns:
        str: image_url, chart_url
    """

    extracted_url: str = capture.Capture(chart_url=create_image_url).capture_image_url()
    image_url: str = create_s3_image_url(extracted_url=extracted_url)

    return image_url, "string"


def create_s3_image_url(extracted_url: str) -> str:
    """
    Cleans the extracted image url by getting image ID
    "https://www.tradingview.com/x/{image_id}/"

    Args:
        extracted_url (str): The extracted URL

    Returns:
        str: Image ID
    """

    image_id: str = ""
    code: str = ""
    parts: list[str] = extracted_url.split(sep="/x/")

    if len(parts) > 1:
        image_id = parts[1].rstrip("/.png")
        code = image_id[0].lower()

    return f"{config.TRADING_IMAGE_URL}/{code}/{image_id}.png"
