# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_api.ipynb.

# %% auto 0
__all__ = ['cli']

# %% ../nbs/03_api.ipynb 1
import pandas as pd
import logging
from fastcore.all import *
from .collab import *
from pathlib import Path
from typing import Literal, Optional
from fastai.collab import CollabDataLoaders, to_device

# %% ../nbs/03_api.ipynb 2
@call_parse
def cli(type: Literal['trian','eval','pred'], 
        ratings_path=Path('./data/ratings.dat'), 
        movies_path=Path('./data/movies.dat'),
        model: Optional[Path]=None,
        out: Path = None):
    
    if not pred: df = read_movielens(ratings_path,movies_path)
    else: df = pd.read_csv()
    dls = CollabDataLoaders.from_df(df, item_name='title', bs=64,valid_pct=0.0)
    m = CollabUserBased()
    
    logging.info(f"loaded ratings and movies from {ratings_path} and {movies_path}")
    if type=='train':
        train(m, dls, out)
    if type=='eval':
        loss = eval(m,dls,model)
        logging.info(f"loss = {loss.item()}")
    if type=='pred':
        preds = pred(m,dls,model)
        preds.save()
