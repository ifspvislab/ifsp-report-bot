"""
Cog for handling events and logging.
"""
import discord
from discord.ext import commands
from discord.ext.commands import Cog

from data import Log, LogData
from services import LogService


class Events(commands.Cog):
    """
    Cog that handles various events and performs logging.
    """

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        Event handler for message events.
        Logs the message author, channel, and content or attachment URL.
        """
        if not message.guild or message.author.bot:
            return

        if LogService().check_student_in_project(student_id=int(message.author.id)):
            if len(message.attachments) > 0:
                date = LogService().formatted_get_date(message=message)
                action = f"{date}-{message.author}-{message.channel}-{message.attachments[0].url}"
                log = Log(
                    discord_id=message.author.id,
                    date=date,
                    action=action,
                )
                LogData().add_log(log)

            else:
                date = LogService().formatted_get_date(message=message)
                action = (
                    f"{date} - {message.author} - {message.channel} - {message.content}"
                )
                log = Log(
                    discord_id=message.author.id,
                    date=date,
                    action=action,
                )
                LogData().add_log(log)

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """
        Event handler for message deletion events.
        Logs the deleted message's author, channel, and content.
        """
        if not message.guild or message.author.bot:
            return

        if LogService().check_student_in_project(student_id=int(message.author.id)):
            date = LogService().formatted_get_date(message=message)
            action = f"{date} - {message.author} - {message.channel} - Deleted: {message.content}"
            log = Log(
                discord_id=message.author.id,
                date=date,
                action=action,
            )
            LogData().add_log(log)

    @Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        """
        Event handler for message edit events.
        Logs the author, channel, and the before and after message content.
        """
        if before.author.bot or before.content == after.content:
            return

        if LogService().check_student_in_project(student_id=int(before.author.id)):
            date = LogService().formatted_get_date(before=before)
            # pylint: disable=line-too-long
            action = f"{date} - {before.author} - {before.channel} - Before: {before.content} - After: {after.content}"
            log = Log(
                discord_id=before.author.id,
                date=date,
                action=action,
            )
            LogData().add_log(log)

    @Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """
        Event handler for interaction events.
        Logs the user and the interaction name.
        """
        if LogService().check_student_in_project(student_id=int(interaction.user.id)):
            date = LogService().formatted_get_date(interaction=interaction)
            action = (
                f"{date} - {interaction.user} - Interaction: {interaction.data['name']}"
            )
            log = Log(
                discord_id=interaction.user.id,
                date=date,
                action=action,
            )
            LogData().add_log(log)

    @Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Event handler for reaction add events.
        Logs the user, reacted emoji, and the reacted message's content.
        """
        if LogService().check_student_in_project(student_id=int(user.id)):
            date = LogService().formatted_get_date()
            # pylint: disable=line-too-long
            action = f"{date} - {user} - Reaction:{reaction.emoji} - Reacted:{reaction.message.content}"
            log = Log(
                discord_id=user.id,
                date=date,
                action=action,
            )
            LogData().add_log(log)
