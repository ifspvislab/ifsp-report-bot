"""
validation module
"""


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
        error = "Coloque um número nos campos **dia**/**mês**/**ano**!"

    elif "1..12" in date:
        error = "Coloque um mês de 01 a 12."

    elif "day" in date:
        error = "Coloque um dia válido para o mês inserido."

    elif "year" in date:
        error = "Insira um ano positivo."
    return error
