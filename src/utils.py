"""
utils
=====

Utility functions for PDF operations.

This module provides utility functions for working with PDF documents.

Functions:
    - save_pdf_bytes(pdf_bytes, file_path): Save the PDF bytes to a file on disk.

"""


def save_pdf_bytes(pdf_bytes, file_path):
    """
    Save the PDF bytes to a file on disk.

    :param pdf_bytes: Bytes of the PDF document.
    :type pdf_bytes: bytes
    :param file_path: Path to the file where the PDF will be saved.
    :type file_path: str
    :return: None
    """
    with open(file_path, "wb") as file:
        file.write(pdf_bytes)
