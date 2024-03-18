# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_embed.ipynb.

# %% auto 0
__all__ = ['Subset', 'EmbeddingDotBias', 'EmbedAdapter']

# %% ../nbs/03_embed.ipynb 3
from fastai.tabular.all import *
from .collab import *

# %% ../nbs/03_embed.ipynb 8
class Subset:
    def __init__(self, ds, indices):store_attr()
    def __getitem__(self,idx):
        return self.ds[self.indices[idx]]
    def __len__(self): return len(self.indices)

# %% ../nbs/03_embed.ipynb 12
class EmbeddingDotBias(Module):
    def __init__(self, n_factors, n_users, n_items, y_range=None):
        self.y_range = y_range
        (self.u_weight, self.i_weight, self.u_bias, self.i_bias) = [Embedding(*o) for o in [
            (n_users, n_factors), (n_items, n_factors), (n_users,1), (n_items,1)
        ]]

    def forward(self, x):
        users,items = x[:,0],x[:,1]
        dot = self.u_weight(users)* self.i_weight(items)
        res = dot.sum(1) + self.u_bias(users).squeeze() + self.i_bias(items).squeeze()
        if self.y_range is None: return res
        return torch.sigmoid(res) * (self.y_range[1]-self.y_range[0]) + self.y_range[0]

# %% ../nbs/03_embed.ipynb 19
class EmbedAdapter:
    def __init__(self, device=None): 
        self.device = ifnone(device, default_device())
        
    def save(self, fname):
        torch.save(self.model, fname)
    
    def load(self, fname):
        obj = torch.load(fname)
        assert obj.__class__ == EmbeddingDotBias, "Class missmatch"
        self.model = obj
    
    def norm(self, x, m, std=None): return (x-m)/std if std else (x-m)/m
    
    @delegates(Learner.fit)
    def fit(self, ds, n_epoch=5, lr=5e-3, wd=0.1, bs=512, **kwargs):
        self.model = EmbeddingDotBias(50, len(ds.user_map), len(ds.movie_map), y_range=(0,5.5)).to(self.device)
        train, val = RandomSubsetSplitter(train_sz=0.9, valid_sz=0.1)(ds)
        dls = DataLoaders.from_dsets(Subset(ds,train),Subset(ds,val), bs=bs)
        self.learn = Learner(dls, self.model, loss_func=MSELossFlat())
        self.learn.fit_one_cycle(n_epoch, lr, wd=wd, **kwargs)

    def predict(self, xb, yb=None):
        with torch.no_grad(): 
            ratings = self.model(xb)
        if yb is not None: return (ratings, F.mse_loss(ratings, yb))
        return ratings
    
    def recommend(self, movies, ratings, topk=5, filter_seen=True):
        movs = self.model.i_weight(movies)
        average_mov = (movs * self.norm(ratings[:,None], ratings.mean())).sum(0)
        res = F.cosine_similarity(average_mov, self.model.i_weight.weight)
        if not filter_seen: return res.topk(topk)
        res = res.topk(topk + len(movies))
        mask = ~torch.isin(res.indices,movies)
        return (res[0][mask][:topk], res[1][mask][:topk])
    
    def similar_movies(self, movie_id: int, topk=5):
        m_v = self.model.i_weight(tensor(movie_id, device=self.device))
        return F.cosine_similarity(m_v, self.model.i_weight.weight).topk(topk+1).indices[1:]