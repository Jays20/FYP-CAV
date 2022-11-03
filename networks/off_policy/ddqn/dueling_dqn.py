import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from parameters import DQN_LEARNING_RATE, DQN_CHECKPOINT_DIR, LATENT_DIM
from autoencoder.variational_autoencoder import VariationalEncoder

class DuelingDQnetwork(nn.Module):
    def __init__(self, n_actions, model):
        super(DuelingDQnetwork, self).__init__()
        self.n_actions = n_actions
        self.checkpoint_file = os.path.join(DQN_CHECKPOINT_DIR, model)

        self.Linear = nn.Sequential(
            nn.Linear(200+3, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU()
        )

        self.V = nn.Linear(64, 1)
        self.A = nn.Linear(64, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=DQN_LEARNING_RATE)
        self.loss = nn.MSELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, x):
        fc = self.Linear(x)
        V = self.V(fc)
        A = self.A(fc)
        return V, A

    def save_checkpoint(self):
        torch.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(torch.load(self.checkpoint_file))
