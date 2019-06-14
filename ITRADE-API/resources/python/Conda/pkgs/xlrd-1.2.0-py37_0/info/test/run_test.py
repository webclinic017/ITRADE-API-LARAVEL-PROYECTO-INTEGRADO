#  tests for xlrd-1.2.0-py37_0 (this is a generated file);
print('===== testing package: xlrd-1.2.0-py37_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import xlrd

wb = xlrd.open_workbook("test.xlsx")
sheet = wb.sheet_by_name("Sheet1")
cell = sheet.cell(0, 0)
print(cell.value)
assert(cell.value == "Hello, World!")
#  --- run_test.py (end) ---

print('===== xlrd-1.2.0-py37_0 OK =====');
