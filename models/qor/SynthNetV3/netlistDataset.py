import os.path as osp
import torch
from zipfile import ZipFile

import pandas as pd
from torch_geometric.data import Dataset, download_url


class NetlistGraphDataset(Dataset):
    def __init__(self, root, filePath, transform=None, pre_transform=None):
        self.filePath = osp.join(root, filePath)
        super(NetlistGraphDataset, self).__init__(root, transform, pre_transform)

    @property
    def processed_file_names(self):
        fileDF = pd.read_csv(self.filePath)
        return fileDF['fileName'].tolist()

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        file_name_zip = self.processed_file_names[idx]
        file_name = osp.splitext(file_name_zip)[0]
        file_path = osp.join(self.processed_dir, file_name)
        data = torch.load(file_path)
        return data