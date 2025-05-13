from openpyxl import load_workbook

def adjust_columns_width(file_name: str) -> None:
    wb = load_workbook(file_name)

    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass

        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(file_name)