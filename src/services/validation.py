"""
validation module
"""

from datetime import datetime


def verify_termination_date_format_error(date):
    """
    Verify what error on the format of the termination date
    occured.

    Args:
        date(str): The date containing the error
    Returns:
        error if the error is detected
        None if the error is not detected
    """
    error = None

    if "invalid literal" in date:
        error = "Coloque um número inteiro nos campos **dia**/**mês**/**ano**!"

    elif "1..12" in date:
        error = "Coloque um mês de 01 a 12."

    elif "day" in date:
        error = "Coloque um dia válido para o mês inserido."

    elif "year" in date:
        error = "Insira um ano positivo."
    return error


def verify_termination_date_period(
    project_start_date, project_end_date, termination_date
):
    """
    Verify if the period of the termination date is within
    the project execution period or if it is a future date or
    today.

    Args:
        project_start_date (date): The start date of the project
        project_end_date (date): The end date of the project
        termination_date (date): The termination date inserted by the member
    Returns:
        error if there is an error in the period of the termination date
        None if there are no errors
    """

    error = None

    days_difference = project_end_date - project_start_date

    input_days_difference = project_end_date - termination_date

    current_time = datetime.now().date()

    if input_days_difference >= days_difference or input_days_difference.days <= 0:
        error = "Insira uma data dentro do período de execução do projeto!"

    elif current_time > termination_date:
        error = "Insira a data de hoje ou uma data futura!"

    return error
