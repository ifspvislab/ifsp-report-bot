"""Cog for Events"""
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from services.log_service import LogService


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if not message.guild or message.author.bot:
            return

        LogService.add_ids(str(message.author))
        date = LogService.get_date(message=message)
        action = f"{date} - {message.author} - {message.channel} - {message.content}"
        LogService.add_logs(str(message.author), date, action)

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if not message.guild or message.author.bot:
            return

        LogService.add_ids(str(message.author))
        date = LogService.get_date(message=message)
        action = f"{date} - {message.author} - {message.channel} - Deleted message: {message.content}"
        LogService.add_logs(str(message.author), date, action)

    @Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        if before.author.bot or before.content == after.content:
            return

        LogService.add_ids(str(before.author))
        date = LogService.get_date(before=before)
        action = f"{date} - {before.author} - {before.channel} - Before message: {before.content} - After message:{after.content}"
        LogService.add_logs(str(before.author), date, action)

    @Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        LogService.add_ids(str(interaction.user))
        date = LogService.get_date(interaction=interaction)
        action = (
            f"{date} - {interaction.user} - Interaction: {interaction.data['name']}"
        )
        LogService.add_logs(str(interaction.user), date, action)

    @Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        LogService.add_ids(str(user))
        # formatted_date = user.created_at.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        action = f"formatted_date - {user} - Reaction: {reaction.emoji}"
        LogService.add_logs(str(user), "formatted_date", action)


async def setup(bot):
    await bot.add_cog(Events(bot))
