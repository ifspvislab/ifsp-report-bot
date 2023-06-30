"""
Cog for handling events and logging.
"""
import discord
from discord.ext import commands
from discord.ext.commands import Cog

from services.log_service import LogService


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

        if LogService.check_student_in_project(
            self=LogService, student_id=int(message.author.id)
        ):
            project_id_by_student = LogService.get_project_id_by_student_id(
                self=LogService, student_id=int(message.author.id)
            )

            if len(message.attachments) > 0:
                date = LogService.formatted_get_date(self=LogService, message=message)
                action = f"{date}-{message.author}-{message.channel}-{message.attachments[0].url}"
                LogService.add_logs(
                    self=LogService,
                    project_id=project_id_by_student,
                    student_id=message.author.id,
                    date=date,
                    action=action,
                )

            else:
                date = LogService.formatted_get_date(self=LogService, message=message)
                action = (
                    f"{date} - {message.author} - {message.channel} - {message.content}"
                )
                LogService.add_logs(
                    self=LogService,
                    project_id=project_id_by_student,
                    student_id=int(message.author.id),
                    date=date,
                    action=action,
                )

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """
        Event handler for message deletion events.
        Logs the deleted message's author, channel, and content.
        """
        if not message.guild or message.author.bot:
            return

        if LogService.check_student_in_project(
            self=LogService, student_id=int(message.author.id)
        ):
            project_id_by_student = LogService.get_project_id_by_student_id(
                self=LogService, student_id=int(message.author.id)
            )

            date = LogService.formatted_get_date(self=LogService, message=message)
            action = f"{date} - {message.author} - {message.channel} - Deleted: {message.content}"
            LogService.add_logs(
                self=LogService,
                project_id=project_id_by_student,
                student_id=int(message.author.id),
                date=date,
                action=action,
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

        if LogService.check_student_in_project(
            self=LogService, student_id=int(before.author.id)
        ):
            project_id_by_student = LogService.get_project_id_by_student_id(
                self=LogService, student_id=int(before.author.id)
            )

            date = LogService.formatted_get_date(self=LogService, before=before)
            action_info = f"{date} - {before.author} - {before.channel}"
            action = (
                action_info + f" - Before: {before.content} - After: {after.content}"
            )
            LogService.add_logs(
                self=LogService,
                project_id=project_id_by_student,
                student_id=int(before.author.id),
                date=date,
                action=action,
            )

    @Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """
        Event handler for interaction events.
        Logs the user and the interaction name.
        """
        if LogService.check_student_in_project(
            self=LogService, student_id=int(interaction.user.id)
        ):
            project_id_by_student = LogService.get_project_id_by_student_id(
                self=LogService, student_id=int(interaction.user.id)
            )

            date = LogService.formatted_get_date(
                self=LogService, interaction=interaction
            )
            action = (
                f"{date} - {interaction.user} - Interaction: {interaction.data['name']}"
            )
            LogService.add_logs(
                self=LogService,
                project_id=project_id_by_student,
                student_id=int(interaction.user.id),
                date=date,
                action=action,
            )

    @Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Event handler for reaction add events.
        Logs the user, reacted emoji, and the reacted message's content.
        """
        if LogService.check_student_in_project(
            self=LogService, student_id=int(user.id)
        ):
            project_id_by_student = LogService.get_project_id_by_student_id(
                self=LogService, student_id=int(user.id)
            )

            date = LogService.formatted_get_date(self=LogService)
            action = f"{date}-{user}-Reaction:{reaction.emoji}-Reacted:{reaction.message.content}"
            LogService.add_logs(
                self=LogService,
                project_id=project_id_by_student,
                student_id=int(user.id),
                date=date,
                action=action,
            )


async def setup(bot):
    """
    Function to add the Events cog to the bot.
    """
    await bot.add_cog(Events(bot))
