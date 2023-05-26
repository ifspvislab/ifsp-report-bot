"""
setup
=======================

This module provides functions for setting up the report module 
and registering the required fonts for PDF reports.

Functions:
    - setup_reports_module(): Set up the report module and register fonts for PDF reports.
    - _register_fonts(): Register specific fonts using the pdfmetrics module.

"""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import settings

logger = settings.logging.getLogger(__name__)


def setup_reports_module():
    """
    Set up the report module and register fonts for PDF reports.

    This function initiates the setup of the report module by registering
    the required fonts using the pdfmetrics module.
    It calls the _register_fonts() function internally to register specific fonts.
    """
    logger.info("starting the setup of the reports module")
    _register_fonts()
    logger.info("report module setup done")


def _register_fonts():
    """
    Register specific fonts using the pdfmetrics module.

    This function registers the Calibri font and its variations by specifying
    the font name and the corresponding font file path.
    """
    pdfmetrics.registerFont(
        TTFont("Calibri", "assets/fonts/calibri/calibri-regular.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Calibri-Bold", "assets/fonts/calibri/calibri-bold.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Calibri-Italic", "assets/fonts/calibri/calibri-italic.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Calibri-Bold-Italic", "assets/fonts/calibri/calibri-bold-italic.ttf")
    )
    logger.info("register fonts executed")
