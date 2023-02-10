import xlsxwriter
from xlsxwriter.exceptions import FileCreateError
import os
from pathlib import Path
from sys import platform

def write_values(values, worksheet, row, col):
    totalEat = 0
    totalCook = 0
    for name, value, percentage, ratio in (values):
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, value[0])
        worksheet.write(row, col + 2, value[1])
        worksheet.write(row, col + 3, str(percentage) + "%")
        worksheet.write(row, col + 4, ratio)
        totalEat += value[0]
        totalCook += value[1]
        row += 1
    averageEat = totalEat // len(values)
    averageCook = totalCook // len(values)
    averagePercentage = round((averageCook/averageEat) * 100, 1)
    averageRatio = round(totalEat / totalCook)
    worksheet.write(row, col, "Average")
    worksheet.write(row, col + 1, averageEat)
    worksheet.write(row, col + 2, averageCook)
    worksheet.write(row, col + 3, str(averagePercentage) + "%")
    worksheet.write(row, col + 4, averageRatio)

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
    worksheet.write(0, col + 4, "Ratio")
    write_values(values, worksheet, row, col)
    workbook.close()
    print('Excel sheet has been made.')


