import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

def to_excel(df: pd.DataFrame, file_name):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name=file_name)
    writer.close()
    processed_data = output.getvalue()
    return processed_data