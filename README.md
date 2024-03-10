# hits-recsys


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

Collaborative filtration with some devops stuff

## Install

``` sh
pip install hits_recsys
```

## How to use

Fill me in please! Don’t forget code examples:

``` python
from hits_recsys.collab import *

ratings = tensor([[0,2,0,0],
                        [0,1,2,0],
                        [1,0,0,3]])
model = CollabUserBased(ratings)
```

``` python
xb,yb = tensor([[1,2]]), tensor(3).view(1,-1)
pred, loss = model.predict(xb,yb)
pred, loss
```

    (tensor([1.4286]), tensor(2.4694))
