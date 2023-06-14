from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

logs = []


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if not message.guild or message.author.bot:
            return

        formatted_date = message.created_at.strftime("%d/%m/%Y %H:%M")
        on_message = f"{formatted_date} - {message.author} - {message.channel} - {message.content}"
        logs.append(on_message)

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if not message.guild or message.author.bot:
            return

        formatted_date = message.created_at.strftime("%d/%m/%Y %H:%M")
        on_message_delete = f"{formatted_date} - {message.author} - {message.channel} - Deleted message: {message.content}"
        logs.append(on_message_delete)

    @Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        if before.author.bot or before.content == after.content:
            return

        formatted_date = before.created_at.strftime("%d/%m/%Y %H:%M")
        on_message_delete = f"{formatted_date} - {before.author} - {before.channel} - Before message: {before.content} - After message:{after.content}"
        logs.append(on_message_delete)

    @Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if not member.guild or member.bot:
            return

        formatted_date = member.created_at.strftime("%d/%m/%Y %H:%M")
        on_member_join = f"{formatted_date} - Member Join: {member}"
        logs.append(on_member_join)

    @Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ) -> None:
        if before == after or before.bot:
            return

        formatted_date = before.created_at.strftime("%d/%m/%Y %H:%M")
        on_member_update = f"{formatted_date} - Before nickname: {before.nick} - Update nick: {after.nick}"
        logs.append(on_member_update)

    @Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        if not member.guild or member.bot:
            return

        formatted_date = member.created_at.strftime("%d/%m/%Y %H:%M")
        on_member_remove = f"{formatted_date} - Removed member: {member}"
        logs.append(on_member_remove)

    @app_commands.command(name="log", description="Create the log file")
    async def log_file(self, interaction: discord.Interaction):
        await create_pdf(logs)

        with open("D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf", "rb") as file:
            await interaction.response.send_message(
                file=discord.File(file, filename="log.pdf")
            )


async def create_pdf(logs):
    doc = SimpleDocTemplate(
        "D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf", pagesize=letter
    )
    styles = getSampleStyleSheet()
    text_style = styles["Normal"]
    content = []

    title = Paragraph("Log file", styles["Heading1"])
    content.append(title)

    for arq in logs:
        log_message = Paragraph(arq, text_style)
        content.append(log_message)

    doc.build(content)


async def setup(bot):
    await bot.add_cog(Events(bot))
