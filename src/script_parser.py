import pandas as pd
from datetime import datetime
from collections import defaultdict
from constants import (
    REGEX_DATE, COLUMN_EMPLOYEE, COLUMN_ARRIVAL, COLUMN_DEPARTURE, TIME_FORMAT, DATE_FORMAT, DATETIME_FORMAT
)
import logging


def check_number_in_unique_file(number, cursor):
    sql_query = "SELECT * FROM unique_file WHERE number = %s"
    cursor.execute(sql_query, (number,))
    result = cursor.fetchone()
    if result:
        return False
    else:
        return True


def get_time_data(time_data):
    comment = ''
    if isinstance(time_data, pd.Series):
        time_data = time_data.iloc[0]
    try:
        time_data = datetime.strptime(time_data, TIME_FORMAT).time()
    except (TypeError, ValueError):
        if isinstance(time_data, str):
            comment = time_data
        time_data = None
    return comment, time_data,


def process_single_excel(file_path, cursor):
    df = pd.read_excel(io=file_path, header=None, nrows=20)
    try:
        position_row = df[df.apply(
            lambda row: row.str.contains(COLUMN_EMPLOYEE, case=False).any(),
            axis=1
        )].index[0]
    except IndexError:
        logging.debug(f'В файле {file_path} нет такой колонки {COLUMN_EMPLOYEE}')
        return

    df_for_sum = df.apply(pd.to_datetime, errors='coerce', format=TIME_FORMAT)
    timestamps = df_for_sum.stack().astype(int) // 10 ** 9
    total_sum = int(timestamps.sum())

    if check_number_in_unique_file(total_sum, cursor):
        df = df[position_row:]
        df.columns = df.iloc[0]
        employee_column = df[COLUMN_EMPLOYEE].reset_index().dropna().iloc[1:]
        result = defaultdict(list)
        for index, row in employee_column.iterrows():
            for date in df.filter(regex=REGEX_DATE).columns.tolist():
                start_col = df.columns.get_loc(date)
                data = df.iloc[:, start_col:]
                try:
                    pos_row_data = data[data.apply(
                        lambda r: r.str.contains(COLUMN_ARRIVAL, case=False).any(),
                        axis=1
                    )].index[0]
                except IndexError:
                    logging.debug(f'В файле {file_path} нет такой колонки {COLUMN_ARRIVAL}')
                    return
                data = data.loc[pos_row_data:]
                data.columns = data.iloc[0]
                data = data.loc[row['index']]
                _, arrival_time = get_time_data(data[COLUMN_ARRIVAL])
                comment, departure_time = get_time_data(data[COLUMN_DEPARTURE])
                date = datetime.strptime(date, DATE_FORMAT).date()
                result.setdefault(
                    row[COLUMN_EMPLOYEE], []
                ).append((date, arrival_time, departure_time, comment))
        return result, total_sum
    return
