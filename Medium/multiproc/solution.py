import re
from string import punctuation

import pandas as pd
from joblib import delayed
from joblib import Parallel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def clear_data(source_path: str, target_path: str, n_jobs: int):
    """Parallel process dataframe

    Parameters
    ----------
    source_path : str
        Path to load dataframe from

    target_path : str
        Path to save dataframe to

    n_jobs : int
        Count of job to process
    """
    data = pd.read_parquet(source_path)
    data = data.copy().dropna().reset_index(drop=True) 
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")
    def out(text):
        #text = str(text)
        re_cat_compiled = re.compile(r"(https?://[^,\s]+,?)|(@[^,\s]+,?)")
        #text = re.sub(r"https?://[^,\s]+,?", "", text)
        #text = re.sub(r"@[^,\s]+,?", "", text)
        text = re_cat_compiled.sub('', text)
        transform_text = text.translate(str.maketrans("", "", punctuation))
        transform_text = re.sub(" +", " ", transfс с orm_text)
        text_tokens = word_tokenize(transform_text)
        lemma_text = [
            lemmatizer.lemmatize(word.lower()) for word in text_tokens
        ]
        cleaned_text = " ".join(
            [str(word) for word in lemma_text if word not in stop_words]
        )
        return cleaned_text
        
    clean = Parallel(n_jobs=n_jobs)(delayed(out)(i) for i in data['text'])
    data["cleaned_text"] = clean
    data.to_parquet(target_path)