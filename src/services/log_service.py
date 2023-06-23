"""Services for log command"""
from datetime import datetime
from reports.styles import events_text_style, events_header_style
import discord
import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate

zone = settings.get_time_zone()

logs = []
users_list = {""}


class LogService:
    def add_logs(user, data, action) -> None:
        log_list = [user, data, action]
        logs.append(log_list)

    def add_ids(id):
        for ids in users_list:
            if id == ids:
                return
        users_list.add(id)

    def date_validation(date: str, expression: str):
        date_list = date.split(" ")
        correct_date = datetime.strptime(date_list[0], "%d/%m/%Y")
        list_date = expression.split("-")

        start_date = datetime.strptime(list_date[0], "%d/%m/%Y")
        end_date = datetime.strptime(list_date[1], "%d/%m/%Y")

        if start_date <= correct_date and correct_date <= end_date:
            return True
        else:
            return False

    def create_pdf(logs, value, expression=""):
        doc = SimpleDocTemplate(
            "D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf", pagesize=letter
        )

        content = []
        title = Paragraph("Log file", events_header_style)
        content.append(title)

        if value == 1:
            for users in users_list:
                user_title = Paragraph(users, events_header_style)
                content.append(user_title)

                for events in logs:
                    for author_events in events:
                        if author_events == users:
                            log_event = Paragraph(events[-1], events_text_style)
                            content.append(log_event)

        if value == 2:
            for users in users_list:
                if users != "":
                    user_title = Paragraph(users, events_header_style)
                    content.append(user_title)

                    for events in logs:
                        for author_events in events:
                            validation = LogService.date_validation(
                                events[1], expression
                            )
                            if validation and author_events == users:
                                log_event = Paragraph(events[-1], events_text_style)
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

    def get_date(
        message: discord.Message = None,
        before: discord.Message = None,
        interaction: discord.Interaction = None,
    ) -> str:
        if message is not None:
            formatted_date = message.created_at.astimezone(zone).strftime(
                "%d/%m/%Y %H:%M"
            )
        elif before is not None:
            formatted_date = before.created_at.astimezone(zone).strftime(
                "%d/%m/%Y %H:%M"
            )
        else:
            formatted_date = interaction.created_at.astimezone(zone).strftime(
                "%d/%m/%Y %H:%M"
            )
        return str(formatted_date)

    def get_logs() -> list:
        return logs

    def get_users() -> set:
        return users_list
