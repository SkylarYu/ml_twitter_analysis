import feature_engineering as fe
import my_globals
import numpy as np
import pandas as pd

from preprocessing import cleaning, preprocess_pipeline

# Always save main dataset outside of the code repo.
# In this case, my data_dir is "../project_data" parallel to "."

def get_sub_dataset(size:int=5000, random_seed:int = 0) -> pd.DataFrame:
    """Generate a subset of the main dataset usinga random seed.
    Saves sub-dataset to a diectory outside of and parallel to main directory. 
    
    :param size: size of subset
    :type size: int, optional. Default to be 5000.
    :param random_seed: random seed
    :type random_seed: int, optional. Default to be 0.
    :rtype: pd.DataFrame
    """
    DATA_PATH = "/".join([my_globals.DATA_DIR, my_globals.MAIN_DATA_NAME])
    DATA_PATH = "../project_data/training.1600000.processed.noemoticon.csv"
    data = pd.read_csv(
        DATA_PATH, 
        # encoding = 'ISO-8859-1',
        encoding = "latin1",
        header = None, 
        names = my_globals.HEADER
    )
    idx = np.random.choice(data.index, size)
    data = data.loc[idx]
    data.to_csv(
        "/".join([my_globals.DATA_DIR, f"twitter_seed{random_seed}.csv"]), 
        index = False,
        encoding = "latin1"
    )
    return data
    
def get_sub_featured_datasets(size:int=5000, random_seed:int = 0) -> pd.DataFrame:
    data = get_sub_dataset(size, random_seed)
    data = cleaning(data)
    data["processed_text"] = data["text"].apply(preprocess_pipeline)
    data["exclaim_freq"] = data["text"].apply(fe.exclaim_freq)
    data["mention_count"] = data["text"].apply(fe.mention_count)
    data["cap_freq"] = data["text"].apply(fe.cap_freq)
    count_tfidf = fe.get_token_features(data, "both")
    data = pd.concat([data, count_tfidf], axis = 1)
    return data
