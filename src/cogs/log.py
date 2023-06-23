import zoneinfo
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from services.coordinator_service import CoordinatorService

zone = zoneinfo.ZoneInfo("America/Recife")
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

        formatted_date = message.created_at.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        # formatted_date1 = message.created_at.astimezone(zone).strftime("%d/%m/%Y")
        action = f"{formatted_date} - {message.author} - {message.channel} - {message.content}"

        await add_logs(str(message.author), formatted_date, action)

    @Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if not message.guild or message.author.bot:
            return

        await add_ids(str(message.author))

        formatted_date = message.created_at.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        action = f"{formatted_date} - {message.author} - {message.channel} - Deleted message: {message.content}"
        await add_logs(str(message.author), formatted_date, action)

    @Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        if before.author.bot or before.content == after.content:
            return

        await add_ids(str(before.author))

        formatted_date = before.created_at.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        action = f"{formatted_date} - {before.author} - {before.channel} - Before message: {before.content} - After message:{after.content}"
        await add_logs(str(before.author), formatted_date, action)

    @Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        await add_ids(str(interaction.user))

        formatted_date = interaction.created_at.astimezone(zone).strftime(
            "%d/%m/%Y %H:%M"
        )
        action = f"{formatted_date} - {interaction.user} - Interaction: {interaction.data['name']}"
        await add_logs(str(interaction.user), formatted_date, action)

    @Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        await add_ids(str(user))

        formatted_date = user.created_at.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        action = f"{formatted_date} - {user} - Reaction: {reaction.emoji}"
        await add_logs(str(user), formatted_date, action)

    @app_commands.command(name="log", description="Create the log file")
    @app_commands.check(CoordinatorService.is_coordinator)
    async def log_file(self, interaction: discord.Interaction, data: str = None):

        if data is None:
            await create_pdf(logs, 1)

        if data is not None:
            try:
                await data_validation("09/10/2023", data)
            except:
                await interaction.response.send_message(
                    "Data incorreta, digite no formato 'data_inicio-data_fim'. Ex:01/09/2023-12/10/2023"
                )

            await create_pdf(logs, 2, data)

        with open("D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf", "rb") as file:
            await interaction.response.send_message(
                file=discord.File(file, filename="log.pdf")
            )

    @log_file.error
    async def log_file_error(self, interaction: discord.Interaction, error):
        """Treating error if it's not the coordinator"""
        await interaction.response.send_message(
            f"Apenas o coordenador tem acesso ao comando! {interaction.user.id}"
        )


async def data_validation(date: str, expression: str):
    date_list = date.split(" ")
    correct_date = datetime.strptime(date_list[0], "%d/%m/%Y")
    list_date = expression.split("-")

    start_date = datetime.strptime(list_date[0], "%d/%m/%Y")
    end_date = datetime.strptime(list_date[1], "%d/%m/%Y")

    if start_date <= correct_date and correct_date <= end_date:
        return True
    else:
        return False


async def create_pdf(logs, value, expression=""):
    doc = SimpleDocTemplate(
        "D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf", pagesize=letter
    )
    styles = getSampleStyleSheet()
    text_style = styles["Normal"]
    title_style = styles["Heading1"]

    content = []

    title = Paragraph("Log file", title_style)
    content.append(title)

    if value == 1:
        for users in users_list:
            user_title = Paragraph(users, title_style)
            content.append(user_title)

            for events in logs:
                for author_events in events:
                    if author_events == users:
                        log_event = Paragraph(events[-1], text_style)
                        content.append(log_event)

    if value == 2:
        for users in users_list:
            if users != "":
                user_title = Paragraph(users, title_style)
                content.append(user_title)

                for events in logs:
                    for author_events in events:
                        validation = await data_validation(events[1], expression)
                        if validation and author_events == users:
                            log_event = Paragraph(events[-1], text_style)
                            content.append(log_event)

    # if value == 3:
    #     for users in users_list:
    #         if(users == expression):
    #             user_title = Paragraph(expression, title_style)
    #             content.append(user_title)

    #     for events in logs:
    #         for author_events in events:
    #             if author_events == expression:
    #                 log_event = Paragraph(events[-1], text_style)
    #                 content.append(log_event)

    doc.build(content)


async def setup(bot):
    await bot.add_cog(Events(bot))
