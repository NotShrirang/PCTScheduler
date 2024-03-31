import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb


def to_excel(df: pd.DataFrame, file_name):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    if ((type(df) is list) and (type(file_name) is list)):
        if len(df) == len(file_name):
            i = 0
            while i < len(df):
                df[i].to_excel(writer, index=False, sheet_name=file_name[i])
                i += 1
    writer.close()
    processed_data = output.getvalue()
    return processed_data
