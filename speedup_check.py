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
nthreads = [1, 4, 8] 
results = [VVENC, EVC, SVT]
names = {
    VVENC: "vvenc",
    EVC: "evc",
    SVT: "svt"
}

def get_total_times(nthreads: str):
    df = pd.DataFrame(columns=["codec", "video", "fps", "number of frames", "qp", "time(s)"])
    equivalent_threads = []
    for codec in results:
        for vcsv in os.listdir(codec):
            for csvf in os.listdir(f"{codec}/{vcsv}"):
                for t in nthreads:
                    t1 = f"_{t}t.csv" in csvf 
                    if t1:
                        equivalent_threads.append(t)
                        im_lazy = pd.read_csv(f"{codec}/{vcsv}/{csvf}")
                        im_lazy = im_lazy.drop(["ypsnr", "upsnr", "vpsnr", "psnr", "bitrate", "optional settings", "number of frames", "resolution"], axis=1)
                        df = df._append(im_lazy, ignore_index=True)
        df['nthreads'] = equivalent_threads
        df = df.sort_values(by=['video', 'nthreads', 'qp'])
        df.to_csv(f"/home/artzmeister/code/ecl/results_sbcci/miscelaneous/checagem{names[codec]}.csv", index=False)
        equivalent_threads = []
        df = pd.DataFrame(columns=["codec", "video", "fps", "number of frames", "qp", "time(s)"])

get_total_times(nthreads)

def individual_comparisons(nthreads: str):
    # Individual comparisons for a given video since the other one was too confusing. 
    ...
