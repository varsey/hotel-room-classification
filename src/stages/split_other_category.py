import pandas as pd

from src.modules.utils import simple_process_item
from src.modules.decorators import duration
from src.modules.helpers import find_similar_pairs
from src.stages.etl import get_hnsw_index

def get_data4index(target: str) -> (pd.DataFrame, pd.DataFrame):
    data4index = pd.read_csv('/opt/app/rates_clean.csv', engine="pyarrow")
    data4index['bedding'] = data4index['bedding'].fillna('undefined')
    data4index['rate_name'] = data4index['rate_name'].fillna('undefined')

    data4index['rate_name_cleaned'] = data4index['rate_name'].apply(lambda x: simple_process_item(x, []))
    data4index['bedding'] = data4index['bedding'].str.replace('twin/twin-or-double', 'double/double-or-twin')

    data4index = pd.concat(
        [
            data4index[data4index[target] == 'double/double-or-twin'].sample(100, random_state=42),
            data4index[~(data4index[target] == 'double/double-or-twin')],
            data4index[~(data4index[target] == 'undefined')],
        ],
        axis='rows',
    ).reset_index(drop=True)
    return data4index

data4index = get_data4index('bedding')
index, vectorizer = get_hnsw_index(get_data4index('bedding'))

def get_closest(name_cleaned):
    query_vector = vectorizer.transform([name_cleaned]).toarray().astype('float32')
    _, indices = find_similar_pairs(index, query_vector, k=1)
    close_pair = data4index.iloc[indices[0][0]].to_dict()
    return close_pair['bedding']

def fix_predict(name_cleaned):
    if name_cleaned == 'undefined':
        return 'undefined'
    elif name_cleaned.count('bed') > 1:
        return 'multiple'
    elif 'bunk' in name_cleaned:
        return 'bunk bed'
    elif 'single bed' in name_cleaned:
        return 'single bed'
    else:
        # TO-DO use get_closest here. It's too clow for now
        return 'undefined'

@duration
def apply_split_to_other_cat(df):
    if 'predict' not in df.columns or 'score' not in df.columns:
        raise ValueError("DataFrame must contain 'value' and 'score' columns")
    mask = (df['predict'] != 'double/double-or-twin')
    df.loc[mask, 'predict'] = df.loc[mask, 'rate_name_cleaned'].apply(fix_predict)
    return df
