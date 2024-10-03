import csv
import sys
import argparse


import pandas as pd
from src.stages.etl import get_train_data, prepare_data
from src.stages.predict import run_prediction
from src.stages.split_other_category import apply_split_to_other_cat
from src.stages.get_view_capacity_column import get_view, get_capacity
from src.modules.h2o_controller import init_h2o, shutdown_h2o

import warnings

from src.stages.train import train_model

warnings.filterwarnings('ignore')

pd.set_option('display.max_colwidth', None)


parser=argparse.ArgumentParser()

parser.add_argument("--content", help="A path to rates CSV file")

args=parser.parse_args()


h2o = init_h2o()

data = get_train_data(target='bedding')
data_d = prepare_data(args.content)

w2v_model, gbm_model = train_model(data, target='bedding')



pre_result = run_prediction(data_d, w2v_model, gbm_model)
pre_result.loc[pre_result.rate_name_cleaned == 'undefined', 'predict'] = 'undefined'
results = apply_split_to_other_cat(pre_result)

results['view'] = results['rate_name_cleaned'].apply(lambda x: get_view(x))
results['capacity'] = results['rate_name_cleaned'].apply(lambda x: get_capacity(x))

results.to_csv('preds.csv', index=False)

shutdown_h2o(h2o)


result = csv.writer(sys.stdout, lineterminator='\n')
result.writerow(
    ['rate_name', 'class', 'quality', 'bathroom', 'bedding', 'capacity', 'club', 'balcony', 'view']
)

with open('preds.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        result.writerow([row[7], '', '', '', row[0], row[10], '', '', row[9]])