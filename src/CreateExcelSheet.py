import xlsxwriter
from xlsxwriter.exceptions import FileCreateError
import os
from pathlib import Path
from sys import platform


def createExcelFile(values):
    workbook = None
    if platform == "linux" or platform == "linux2":
        # Linux
        workbook = xlsxwriter.Workbook("/results/EetlijstData.xlsx")
    elif platform == "win32":
        # Windows...
        workbook = xlsxwriter.Workbook("EetlijstData.xlsx")

    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    worksheet.write(0, col, "Name")
    worksheet.write(0, col + 1, "Joined dinner")
    worksheet.write(0, col + 2, "Cooked")
    worksheet.write(0, col + 3, "Percentage")

    for name, value, percentage in (values):
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, value[0])
        worksheet.write(row, col + 2, value[1])
        worksheet.write(row, col + 3, percentage)
        row += 1

    workbook.close()
    print('Excel sheet has been made.')
