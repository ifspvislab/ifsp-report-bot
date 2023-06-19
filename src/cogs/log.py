from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

logs = []
users_list = {""}


async def add_logs(user, data, action) -> None:
    log_list = [user, data, action]
    logs.append(log_list)


async def add_ids(id):
    for ids in users_list:
        if id == ids:
            return
    users_list.add(id)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if not message.guild or message.author.bot:
            return

        await add_ids(str(message.author))

        formatted_date = message.created_at.strftime("%d/%m/%Y %H:%M")
        action = f"{formatted_date} - {message.author} - {message.channel} - {message.content}"
        await add_logs(str(message.author), formatted_date, action)

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if not message.guild or message.author.bot:
            return

        await add_ids(str(message.author))

        formatted_date = message.created_at.strftime("%d/%m/%Y %H:%M")
        action = f"{formatted_date} - {message.author} - {message.channel} - Deleted message: {message.content}"
        await add_logs(str(message.author), formatted_date, action)

    @Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        if before.author.bot or before.content == after.content:
            return

        await add_ids(str(before.author))

        formatted_date = before.created_at.strftime("%d/%m/%Y %H:%M")
        action = f"{formatted_date} - {before.author} - {before.channel} - Before message: {before.content} - After message:{after.content}"
        await add_logs(str(before.author), formatted_date, action)

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
    title_style = styles["Heading1"]

    content = []

    title = Paragraph("Log file", title_style)
    content.append(title)

    for users in users_list:
        user_title = Paragraph(users, title_style)
        content.append(user_title)
        for events in logs:
            for author_events in events:
                if author_events == users:
                    log_event = Paragraph(events[-1], text_style)
                    content.append(log_event)

    doc.build(content)


async def setup(bot):
    await bot.add_cog(Events(bot))
