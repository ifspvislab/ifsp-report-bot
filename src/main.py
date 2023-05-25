"""
IFSP Report Bot

This module provides functionality for generating and managing monthly reports for
the IFSP (Instituto Federal de Educação, Ciência e Tecnologia de São Paulo) 
institution.

The module consists of the following main components:

- `reports`: This submodule contains functions for generating monthly reports in PDF
  format. The `generate_monthly_report` function is the main entry point for 
  generating a monthly report.

- `utils`: This submodule contains utility functions for saving PDF bytes to a file, 
  handling file operations, and other related operations.

Usage:
    To generate a monthly report, run the `main` function in this module. The `main` 
    function calls the `generate_monthly_report` function from the `reports` submodule,
    generates a PDF report, and saves it using the `utils` submodule.

Dependencies:
    This module requires the following dependencies:
    - `utils`: A submodule providing utility functions for PDF generation and file 
      operations.
    - `reports`: A submodule containing the report generation logic and styles.

Note:
    Before running the `main` function, make sure to set up the necessary environment,
    including the required data files and configurations.

Author:
    Domingos Latorre

Version:
    1.0.0
"""

import utils
import reports


def main():
    """
    Main function that generates and saves a monthly report PDF.

    This function is the entry point of the IFSP Report Bot. It calls the `generate_monthly_report`
    function from the `reports` module to generate a monthly report in PDF format. The generated PDF
    is then saved using the `save_pdf_bytes` function from the `utils` module.

    Note:
        The generated PDF will be saved as "monthy_report_example.pdf".

    """
    pdf_bytes = reports.generate_monthly_report()
    utils.save_pdf_bytes(pdf_bytes, "monthy_report_example.pdf")


if __name__ == "__main__":
    main()
