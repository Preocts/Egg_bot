""" Egg Bot, Discord Modular Bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import logging
import discord

import dotenv

from eggbot import core_entities


# Globals
logger = logging.getLogger(__name__)  # Logger
# TODO: Configure basic logger and file logger

eggbot_config = core_entities.CoreConfig()  # Configuration for bot
eventsub = core_entities.EventSub()  # Event Pub/Sub framework

dotenv.load_dotenv  # Load .env if exist

DISCORD_TOKEN = os.environ.get("discord_api_key")

# Setup Discord Client configuration
# TODO: intents should be in configuration file
intents = discord.Intents.default()
intents.members = True
discord_client = discord.Client(status="online", intents=intents)


def load_config() -> bool:
    """ Load configuration """
    global eggbot_config
    logger.info("Opening configuration...")
    eggbot_config.load()
    if not eggbot_config.config:
        logger.warning("Configuration not found!")
        # TODO: Add method to pull file path for output
        return False
    logger.info(
        "Configuration file loaded with " f"{len(eggbot_config.config)} keys."
    )
    return True


@discord_client.event
async def on_member_join(member) -> bool:
    """ Triggered on all join events """
    global eventsub
    if member.id == discord_client.user.id:
        logger.warning("on_member_join(), Saw ourselves join, that's weird.")
        return False
    if member.bot:
        logger.info("on_member_join(), Bot join detected, ignoring.")
        return False

    for subbed in eventsub.event_list("on_join"):
        subbed(member)

    return True


@discord_client.event
async def on_message(message) -> bool:
    """ Triggered on all message events """
    global eventsub
    if message.author.id == discord_client.user.id:
        logger.debug("on_message(), Ignoring ourselves.")
        return False

    if message.author.bot:
        logger.info("on_message(), Bot chat, ignoring.")
        return False

    for subbed in eventsub.event_list("on_message"):
        subbed(message)

    return True


def main() -> None:
    global eggbot_config
    global DISCORD_TOKEN
    load_config()

    discord_client.run(DISCORD_TOKEN)

    eggbot_config = None
    pass


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
