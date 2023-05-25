"""
utils.py - Utility functions for PDF operations.

This module provides utility functions for working with PDF documents.

Functions:
    save_pdf_bytes(pdf_bytes, file_path):
        Save the PDF bytes to a file on disk.
"""


def save_pdf_bytes(pdf_bytes, file_path):
    """
    Save the PDF bytes to a file on disk.

    Args:
        pdf_bytes (bytes): Bytes of the PDF document.
        file_path (str): Path to the file where the PDF will be saved.

    Returns:
        None
    """
    with open(file_path, "wb") as file:
        file.write(pdf_bytes)
