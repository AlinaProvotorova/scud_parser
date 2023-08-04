import pandas as pd
from datetime import datetime
from collections import defaultdict
from constants import (
    REGEX_DATE, COLUMN_EMPLOYEE, COLUMN_ARRIVAL, COLUMN_DEPARTURE, TIME_FORMAT, DATE_FORMAT
)


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


def process_single_excel(file_path):
    df = pd.read_excel(io=file_path, header=None, nrows=20)
    position_row = df[df.apply(
        lambda row: row.str.contains(COLUMN_EMPLOYEE, case=False).any(),
        axis=1
    )].index[0]
    df = df[position_row:]
    df.columns = df.iloc[0]
    employee_column = df[COLUMN_EMPLOYEE].reset_index().dropna().iloc[1:]
    result = defaultdict(list)
    for index, row in employee_column.iterrows():
        for date in df.filter(regex=REGEX_DATE).columns.tolist():
            start_col = df.columns.get_loc(date)
            data = df.iloc[:, start_col:]
            pos_row_data = data[data.apply(
                lambda r: r.str.contains(COLUMN_ARRIVAL, case=False).any(),
                axis=1
            )].index[0]
            data = data.loc[pos_row_data:]
            data.columns = data.iloc[0]
            data = data.loc[row['index']]
            _, arrival_time = get_time_data(data[COLUMN_ARRIVAL])
            comment, departure_time = get_time_data(data[COLUMN_DEPARTURE])
            date = datetime.strptime(date, DATE_FORMAT).date()
            result.setdefault(
                row[COLUMN_EMPLOYEE], []
            ).append((date, arrival_time, departure_time, comment))
    return result
