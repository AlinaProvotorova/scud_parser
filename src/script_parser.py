from collections import defaultdict
from datetime import datetime

import pandas as pd

from constants import (
    EXCEL_COLUMN_ARRIVAL, EXCEL_COLUMN_DEPARTURE, EXCEL_COLUMN_EMPLOYEE,
    EXEL_REGEX_DATE, EXCEL_REGEX_DATE, EXCEL_REGEX_TIME
)

ERROR_NO_COLUMN = 'В файле {} нет такой колонки {}'
ERROR_FILE_NOT_UNIQUE = "Файл был ранее проверен"
ERROR_FILE_DATA = "В файле {} не было найдено нужных данных"


def check_number_in_unique_file(number, cursor):
    sql_query = "SELECT * FROM unique_file WHERE number = %s"
    cursor.execute(sql_query, (number,))
    result = cursor.fetchone()
    if result:
        raise ValueError(ERROR_NO_COLUMN.format(number))


def get_time_or_comment(time_data):
    comment = ''
    if isinstance(time_data, pd.Series):
        time_data = time_data.iloc[0]
    try:
        time_data = datetime.strptime(time_data, EXCEL_REGEX_TIME).time()
    except (TypeError, ValueError):
        if isinstance(time_data, str):
            comment = time_data
        time_data = None
    return comment, time_data,


def get_total_sum_file(df):
    df = df.apply(pd.to_datetime, errors='coerce', format=EXCEL_REGEX_TIME)
    timestamps = df.stack().astype(int) // 10 ** 9
    return int(timestamps.sum())


def get_position_row(df, file_path, column):
    try:
        position_row = df[df.apply(
            lambda row: row.str.contains(column, case=False).any(),
            axis=1
        )].index[0]
        return position_row
    except IndexError:
        raise ValueError(ERROR_NO_COLUMN.format(file_path, column))


def process_employee_data(df, file_path):
    employee_column = df[EXCEL_COLUMN_EMPLOYEE].reset_index().dropna().iloc[1:]
    date_columns = df.filter(regex=EXCEL_REGEX_DATE).columns.tolist()
    if employee_column.empty or not date_columns:
        raise ValueError(ERROR_FILE_DATA.format(file_path))
    data = df.iloc[:, df.columns.get_loc(date_columns[0]):]
    position_row = get_position_row(data, file_path, EXCEL_COLUMN_ARRIVAL)

    employee_data = defaultdict(list)
    for _, row in employee_column.iterrows():
        for date in date_columns:
            data = df.iloc[:, df.columns.get_loc(date):]
            data = data.loc[position_row:]
            data.columns = data.iloc[0]
            data = data.loc[row['index']]
            _, arrival_time = get_time_or_comment(data[EXCEL_COLUMN_ARRIVAL])
            comment, departure_time = get_time_or_comment(
                data[EXCEL_COLUMN_DEPARTURE]
            )
            date = datetime.strptime(date, EXEL_REGEX_DATE).date()
            employee_data.setdefault(
                row[EXCEL_COLUMN_EMPLOYEE], []
            ).append((date, arrival_time, departure_time, comment))
    return employee_data


def process_single_excel(file_path, cursor):
    df = pd.read_excel(io=file_path, header=None)
    position_row = get_position_row(df, file_path, EXCEL_COLUMN_EMPLOYEE)
    total_sum = get_total_sum_file(df)
    check_number_in_unique_file(total_sum, cursor)
    df = df[position_row:]
    df.columns = df.iloc[0]
    employee_data = process_employee_data(df, file_path)
    return employee_data, total_sum
