import pandas as pd
from tqdm import tqdm

date_pattern = r"\d{2}\.\d{2}\.\d{4}"


def process_single_excel(file_path, cursor):
    df = pd.read_excel(io=file_path, header=None)
    position_row = df[df.apply(lambda row: row.str.contains('сотрудник', case=False).any(), axis=1)].index[0]
    df = df[position_row:]
    df.columns = df.iloc[0]
    sotrudnik_column = df['Сотрудник'].reset_index().dropna().iloc[1:]
    dates = df.filter(regex='\d{2}\.\d{2}\.\d{4}').columns.tolist()
    for index, row in tqdm(sotrudnik_column.iterrows()):
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
