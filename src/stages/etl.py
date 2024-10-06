import os
import pandas as pd

from src.modules.utils import simple_process_item


def get_train_data(target: str) -> (pd.DataFrame, pd.DataFrame):
    data = pd.read_csv(f'{os.getcwd()}/data/sample_clean.csv', engine="pyarrow")
    data['bedding'] = data['bedding'].fillna('undefined')
    data['rate_name'] = data['rate_name'].fillna('undefined')

    data['rate_name_cleaned'] = data['rate_name'].apply(lambda x: simple_process_item(x, []))
    data['bedding'] = data['bedding'].str.replace('twin/twin-or-double', 'double/double-or-twin')

    data['bedding'] = data['bedding'].str.replace('multiple', 'other')
    data['bedding'] = data['bedding'].str.replace('single bed', 'other')
    data['bedding'] = data['bedding'].str.replace('bunk bed', 'other')
    data['bedding'] = data['bedding'].str.replace('undefined', 'other')

    data = pd.concat(
        [
            data[data[target] == 'double/double-or-twin'].sample(200, random_state=42),
            data[~(data[target].str.contains('double/double-or-twin|undefined'))],
        ],
        axis='rows',
    ).reset_index(drop=True)

    return data


def prepare_data(path) -> pd.DataFrame:
    data_d = pd.read_csv(path, engine="pyarrow")
    data_d['bedding'] = data_d['bedding'].fillna('undefined')
    data_d['rate_name'] = data_d['rate_name'].fillna('undefined')

    data_d['view'] = data_d['view'].fillna('undefined')
    data_d['capacity'] = data_d['capacity'].fillna('undefined')

    data_d['rate_name_cleaned'] = data_d['rate_name'].apply(lambda x: simple_process_item(x, []))
    data_d['bedding'] = data_d['bedding'].str.replace('twin/twin-or-double', 'double/double-or-twin')

    data_d = data_d[~(data_d['rate_name_cleaned'] == 'name')].reset_index(drop=True)
    return data_d
