import re
import string

import h2o


flt_chars = []

def remove_punctuation(input_string):
    combined_punctuation = string.punctuation + ''.join(flt_chars)
    combined_punctuation = ''.join([x for x in combined_punctuation if x not in ('/', '-')])
    translator = str.maketrans(combined_punctuation, ' ' * len(combined_punctuation))
    return input_string.translate(translator)

def split_on_capital_letters(word):
    return re.findall(r'[A-Z][a-z]*|[A-Z]+', word)

def lowercase_all_capital_words(sent):
    res = []
    for word in sent.split():
        if word.isupper():
             res.append(word.lower())
        else:
            res.append(word)
    return ' '.join(res)

split_pattern = r'(?<!^)(?=[A-Z])'
def simple_process_item(x: str, exclude: list):
    if x is None:
        return  ''
    x = lowercase_all_capital_words(x)
    x = ' '.join([w for w in re.split(split_pattern, x)])
    x = x.lower()
    x = remove_punctuation(x)
    item = ' '.join(re.split(r'(\d+)', x))
    while item.count(2 * " ") > 0:
        item = item.replace(2 * " ", " ")
    item = item.replace(' .', '.').replace('. ', '.')
    return ' '.join([x for x in item.split() if x not in exclude])

def tokenize(sentences):
    return sentences.tokenize(" ")

# @duration
def predict(job_title, w2v, gbm):
    words = tokenize(h2o.H2OFrame(job_title).ascharacter())
    job_title_vec = w2v.transform(words, aggregate_method="AVERAGE")
    return gbm.predict(test_data=job_title_vec)


def compare_dicts(dict1, dict2):
    differences = {}
    all_keys = set(dict1.keys()).union(set(dict2.keys()))

    for key in all_keys:
        value1 = dict1.get(key)
        value2 = dict2.get(key)

        if value1 != value2:
            differences[key] = {'dict1': value1, 'dict2': value2}

    return differences