import torch 
import torch.nn as nn 
import numpy as np 
from Attention import attention, multiheadAttention 

class EncoderLayer(nn.Module): 
    def __init__(self, input_dim, d_model, n_layers, n_head): 
        super().__init__(self) 
        self.input_dim = input_dim
        self.d_model = d_model 
        self.n_layers = n_layers 
        self.n_head = n_head
        self.input_embedding = nn.Linear(input_dim, d_model)
        self.self_attention = multiheadAttention(d_model, n_head)


class Encoder(nn.Module):
    def __init__(self, input_dim, d_model, n_layers): 
        super().__init__() 
        self.encoder_layer = EncoderLayer()


    def forward(self)


