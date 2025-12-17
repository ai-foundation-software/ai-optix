# SPDX-FileCopyrightText: 2025 ai-foundation-software
# SPDX-License-Identifier: Apache-2.0

import time
import torch
from torch.utils.data import Dataset, DataLoader

class SlowDataset(Dataset):
    def __init__(self, size=100):
        self.size = size
        
    def __len__(self):
        return self.size
        
    def __getitem__(self, idx):
        # Simulate slow IO / CPU processing
        time.sleep(0.2) 
        return torch.randn(1024)

def train():
    print("Starting Slow Training...")
    dataset = SlowDataset(size=50) # 50 items
    # num_workers=0 causes main thread to wait for every item (Slow)
    loader = DataLoader(dataset, batch_size=5, num_workers=0)
    
    for batch in loader:
        # Simulate fast GPU compute
        # time.sleep(0.01)
        pass
    print("Training Complete.")

if __name__ == "__main__":
    train()
