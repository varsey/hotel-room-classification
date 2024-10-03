import pandas as pd
from h2o import H2OFrame

from h2o.estimators.word2vec import H2OWord2vecEstimator
from h2o.estimators.gbm import H2OGradientBoostingEstimator

from src.modules.utils import tokenize

COL_TYPES = ["string", "enum", "enum", "enum", "enum", "enum", "enum", "enum", "enum", "enum", "enum", "string"]


def train_model(data: pd.DataFrame, target: str):
    rooms_desc = H2OFrame(data, column_types = COL_TYPES)

    words = tokenize(rooms_desc["rate_name_cleaned"])

    w2v_model = H2OWord2vecEstimator(sent_sample_rate=0.0, epochs=10)
    w2v_model.train(training_frame=words)

    rooms_desc_vecs = w2v_model.transform(words, aggregate_method = "AVERAGE")

    h2o_data = rooms_desc.cbind(rooms_desc_vecs)

    gbm_model = H2OGradientBoostingEstimator(seed=1234)
    gbm_model.train(x=rooms_desc_vecs.names, y=target, training_frame = h2o_data)

    return w2v_model, gbm_model
