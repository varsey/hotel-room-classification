import pandas as pd

from src.modules.decorators import duration
from src.modules.utils import predict
N = 40_000

@duration
def run_prediction(data_d, w2v_model, gbm_model):
    r_name = data_d['rate_name'].to_list()
    cand = data_d['rate_name_cleaned'].to_list()
    b_cand = data_d['bedding'].to_list()
    v_cand = data_d['view'].to_list()
    c_cand = data_d['capacity'].to_list()

    result = pd.DataFrame()
    for indx in range(0, len(cand), N):
        # print('###', indx)
        documents_preds = predict(cand[indx:indx + N], w2v_model, gbm_model).as_data_frame()
        documents = pd.concat([
            documents_preds,
            pd.DataFrame(cand[indx:indx + N], columns=['rate_name_cleaned']),
            pd.DataFrame(b_cand[indx:indx + N], columns=['bedding']),
            pd.DataFrame(v_cand[indx:indx + N], columns=['view_orig']),
            pd.DataFrame(c_cand[indx:indx + N], columns=['capacity_orig']),
            pd.DataFrame(r_name[indx:indx + N], columns=['rate_name']),
        ], axis='columns')
        documents['score'] = documents[documents.columns[1:-5]].max(axis=1)
        result = pd.concat([
            result,
            documents,
        ], axis='rows')

    return result