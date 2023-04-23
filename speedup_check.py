"""
This file was used to double check the results of the encodings in regards to time, for the sake of making a fair speedup comparison. 
Particularly, we are interested in the results of SVT when it uses a single thread.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os 

SVT = "/home/artzmeister/code/ecl/results_sbcci/output/svt/3/csv"
VVENC = "/home/artzmeister/code/ecl/results_sbcci/output/vvcodec/medium/csv"
EVC = "/home/artzmeister/code/ecl/results_sbcci/output/evc/slow/csv"
results = [SVT, VVENC, EVC]

def get_total_times():
    df = pd.DataFrame(columns=["codec", "video", "resolution", "fps", "number of frames", "qp", "time(s)"])
    for codec in results:
        for vcsv in os.listdir(codec):
            for csvf in os.listdir(f"{codec}/{vcsv}"):
                t1 = "_1t.csv" in csvf 
                if t1:
                    im_lazy = pd.read_csv(f"{codec}/{vcsv}/{csvf}")
                    im_lazy = im_lazy.drop(["ypsnr", "upsnr", "vpsnr", "psnr", "bitrate", "optional settings"], axis=1)
                    df = df._append(im_lazy, ignore_index=True)
    df.to_csv("/home/artzmeister/code/ecl/results_sbcci/miscelaneous/checagem.csv", index=False)


get_total_times()
