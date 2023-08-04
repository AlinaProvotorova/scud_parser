import os
import pandas as pd
import mysql.connector
import argparse
import re
import numpy as np

from utils import config, logging


def process_excel_files(excel_directory):
    conn = mysql.connector.connect(
        host=config['database']['host'],
        user=config['database']['username'],
        password=config['database']['password'],
        database=config['database']['database_name']
    )
    cursor = conn.cursor()

    for filename in os.listdir(excel_directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(excel_directory, filename)
            process_single_excel(file_path, cursor)

    conn.commit()
    cursor.close()
    conn.close()


date_pattern = r"\d{2}\.\d{2}\.\d{4}"


def process_single_excel(file_path, cursor):
    df = pd.read_excel(io=file_path, header=None, nrows=13)
    position_row = df[df.apply(lambda row: row.str.contains('сотрудник', case=False).any(), axis=1)].index[0]
    df = df[position_row:]
    df.columns = df.iloc[0]
    sotrudnik_column = df['Сотрудник'].reset_index().dropna().iloc[1:]
    dates = df.filter(regex='\d{2}\.\d{2}\.\d{4}').columns.tolist()
    for index, row in sotrudnik_column.iterrows():
        print(row['Сотрудник'])
        for date in dates:
            print(date)
            start_col = df.columns.get_loc(date)
            data = df.iloc[:, start_col:]
            position_row_data = data[data.apply(lambda r: r.str.contains('вход', case=False).any(), axis=1)].index[0]
            data = data.loc[position_row_data:]
            data.columns = data.iloc[0]
            data = data.loc[row['index']]
            vhod = data['Вход']
            if isinstance(vhod, pd.Series):
                vhod = vhod.iloc[0]
            print(f'Вход: {vhod}')
            exit = data['Выход']
            if isinstance(exit, pd.Series):
                exit = exit.iloc[0]
            print(f'Выход: {exit}')

    # # col = df.iloc[:, start_col: end_col]
    # for index, row in sotrudnik_column.iterrows():
    #     print(index, row['Сотрудник'])

    #
    #     print(f'Сотрудник: {sotrudnik}')
    #     for _, row in date_columns.iterrows():
    #         print(_, row)
    #     for date_column in date_columns:
    #         print(date_column.loc[])
    # print(date_columns)
    # data_df = data_df.dropna(how='all')
    # data_df = data_df.dropna(subset=[data_df.columns[0]])
    # print(data_df)
    # data_df = df.iloc[:, position_row + 1:]
    # data_df = data_df.dropna(subset=[data_df.columns[0]])
    #
    # # Итерация по строкам таблицы для обработки данных
    # for _, row in data_df.iterrows():
    #     employee_position = row[0]
    #     employee_name = row[5]
    #     work_date = row[6]
    #     arrival_time = row[10]
    #     departure_time = row[11]
    #     additional_info = row[1]

    # Дополнительная обработка данных или операции с базой данных, если необходимо
    # Например, вы можете вставить извлеченные данные в базу данных, используя предоставленный курсор.

    # Вывод извлеченных данных для примера
    # print(f"Должность: {employee_position}")
    # print(f"Фамилия сотрудника: {employee_name}")
    # print(f"Дата рабочего дня: {work_date}")
    # print(f"Время прихода в офис: {arrival_time}")
    # print(f"Время ухода из офиса: {departure_time}")
    # print(f"Дополнительное обоснование: {additional_info}")
    # print()
    # attendance_data = []
    # for index, row in df.iterrows():
    #     last_name = row['Unnamed: 4']
    #     work_date = row['Unnamed: 5']
    #     arrival_time = row['Unnamed: 22']
    #     departure_time = row['Unnamed: 23']
    #     comment = row['Unnamed: 24']
    #     attendance_data.append((last_name, work_date, arrival_time, departure_time, comment))
    # print(df)
    # print(attendance_data)
    # for _, row in df.head().iterrows():
    #     for i in row:
    #         if isinstance(i, str) and "период" in i.lower():
    #             start_date, end_date = re.findall(date_pattern, i)
    #             print("Начало периода:", start_date)
    #             print("Конец периода:", end_date)
    #             break
    # print(df)

    # for _, row in df.iterrows():
    #     print(row)
    # last_name = row['Фамилия сотрудника']
    # work_date = row['Дата рабочего дня']
    # arrival_time = row['Время прихода']
    # departure_time = row['Время ухода']
    # comment = row['Дополнительное текстовое обоснование']
    #
    # sql = """
    #     INSERT IGNORE INTO attendance (employee_id, work_date, arrival_time, departure_time, comment)
    #     VALUES (%s, %s, %s, %s, %s)
    # """
    #
    # cursor.execute(sql, (last_name, work_date, arrival_time, departure_time, comment))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Excel files and export data to a MySQL database.')
    parser.add_argument('excel_directory', help='Path to the directory containing Excel files to process.')

    args = parser.parse_args()
    process_excel_files(args.excel_directory)
