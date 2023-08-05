"""
Cog for handling events and logging.
"""
import discord
from discord.ext import commands
from discord.ext.commands import Cog

from services import LogService


class Events(commands.Cog):
    """
    Cog that handles various events and performs logging.
    """

    def __init__(self, log_service: LogService):
        self.log_service = log_service

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        Event handler for message events.
        Logs the message author, channel, and content or attachment URL.
        """
        if not message.guild or message.author.bot:
            return

        if len(message.attachments) > 0:
            action = (
                f"{message.author} - {message.channel} - {message.attachments[0].url}"
            )
            self.log_service.generate_log(
                action=action,
                student_id=message.author.id,
                date=message.created_at,
            )
        else:
            action = f"{message.author} - {message.channel} - {message.content}"
            self.log_service.generate_log(
                action=action,
                student_id=message.author.id,
                date=message.created_at,
            )

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """
        Event handler for message deletion events.
        Logs the deleted message's author, channel, and content.
        """
        if not message.guild or message.author.bot:
            return

        action = f"{message.author} - {message.channel} - Deleted: {message.content}"
        self.log_service.generate_log(
            action=action,
            student_id=message.author.id,
            date=message.created_at,
        )

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
        # pylint: disable=line-too-long
        action = f"{before.author} - {before.channel} - Before: {before.content} - After: {after.content}"
        self.log_service.generate_log(
            action=action,
            student_id=before.author.id,
            date=before.created_at,
        )

    @Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """
        Event handler for interaction events.
        Logs the user and the interaction name.
        """
        try:
            action = f"{interaction.user} - Interaction: {interaction.data['name']}"

            self.log_service.generate_log(
                action=action,
                student_id=interaction.user.id,
                date=interaction.created_at,
            )
        except KeyError:
            return

    @Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Event handler for reaction add events.
        Logs the user, reacted emoji, and the reacted message's content.
        """
        action = (
            f"{user} - Reaction: {reaction.emoji} - Reacted: {reaction.message.content}"
        )
        self.log_service.generate_log(
            action=action,
            student_id=user.id,
        )
