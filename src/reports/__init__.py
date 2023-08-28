"""
Reports Package

This package provides functionality for generating and managing reports.

Modules:
- setup: Contains setup functions for the reports package.
- styles: Contains styles and formatting settings for the reports.
- monthly_report: Provides the MonthlyReport class for generating monthly reports.

Functions:
- setup_reports_module: Sets up the reports module.

Classes:
- MonthlyReportData: Represents the data for a monthly report.
- MonthlyReport: Generates monthly reports.
- SemesterReportData: Represents the data for a semester report.
- SemesterReport: Generates semester reports.

"""

from . import styles
from .attendance_sheet import AttendanceSheet, AttendanceSheetData
from .log_report import LogReport, LogReportData
from .monthly_report import MonthlyReport, MonthlyReportData
from .semester_report import SemesterReport, SemesterReportData
from .setup import setup_reports_module
from .termination_statement import (TerminationStatement,
                                    TerminationStatementData)

setup_reports_module()
