from openpyxl import load_workbook
from openpyxl.styles import Alignment


def adjust_columns_width(file_name: str) -> None:
    wb = load_workbook(file_name)

    ws = wb.active

    for col_idx, column in enumerate(ws.columns, 1):
        column_letter = column[0].column_letter

        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass

        if col_idx == 1:
            ws.column_dimensions[column_letter].width = 100
            for cell in column:
                cell.alignment = Alignment(wrap_text=True)
        else:
            ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(file_name)