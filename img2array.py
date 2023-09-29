import os
import glob
from pathlib import Path

import pandas as pd
import numpy as np
import tifffile as tif

def path_to_img_array(uuid, scale, type: str = 'T',save=True) -> array:
    img_array_ls = []
    path = f'/GPUFS/sysu_jhluo_1/wangyh/data/BLCA_TMB/patches_annotated/CN_patches/*/{uuid}/{scale}X'
    os.chdir(path)
    assert type in ['T','nonT'], 'invalid tissue type'
    try:
        tifs = glob.glob(path + f'{type}*.tiff')
        for t in tifs:
            img = tif.imread(t)
            tif_coord = Path(t).name.split('_')[1] + '_' + Path(t).name.split('_')[2]
            img_array_ls.append((tif_coord,img))
            img_array = np.array(img_array_ls)
        if save:s
            np.save(f'{scale}X_array.npy', img_array)
        return img_array
    except Exception as e:
        print(f'wrong in func<path_to_img_array> when handle uuid {uuid}, log: {e}')
        return None

def main():
    full = pd.read_csv('../config/patch_info.csv')
    uuids = full['dir_uuid']
    for uuid in uuids:
        for scale in [10,20]:
            _ = path_to_img_array(uuid,scale)