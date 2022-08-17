import model 

import pandas as pd


def extract_data_test():
    actual_df = model.extract_data()

    assert type(actual_df) == pd.DataFrame