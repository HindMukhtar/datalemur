import torch 
import torch.nn as nn 
import math 

class attention(nn.Module): 
    def __init__(self, d_model, d_k, d_v):
        super().__init__() 
        self.wq = nn.Linear(d_model, d_k, bias = False)
        self.wk = nn.Linear(d_model, d_k, bias = False)
        self.wv = nn.Linear(d_model, d_v, bias = False)

    def forward(self, x, y=None):
        if y is None: 
            y = x
        Q = self.wq(x) # (seq_len, d_k)
        K = self.wk(y) # (seq_len, d_k)
        V = self.wv(y) # (seq_len, d_v)

        scores = Q @ K.transpose(-2, -1)/math.sqrt(K.shape[-1])
        weights = torch.softmax(scores, dim=-1)
        outputs = weights @ V

        return weights, outputs 
    

class multiheadAttention(nn.Module): 
    def __init__(self, d_model, n_head): 
        super().__init__()

        assert d_model % n_head == 0 # must be divisible by n_head 

        d_k = d_v = d_model//n_head 
        self.heads = nn.ModuleList([attention(d_model, d_k, d_v) for _ in range(n_head)])
        self.wo = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, y=None): 
        if y is None: 
            y = x 

        all_outputs = []
        all_weights = []

        for head in self.heads: 
            w, out = head(x, y)
            all_weights.append(w)
            all_outputs.append(out) 
        
        output = torch.concat(all_outputs, dim = -1) # (..., seq_len, d_model)

        return all_weights, self.wo(output)
        
