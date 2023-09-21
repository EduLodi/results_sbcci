import matplotlib.pyplot as plt
import matplotlib as mpl
import os

"""
This script generates the speedup barplot used in our SBCCI 2023 article.
Speedup here means that we're dividing the old execution time (single-threaded)
by the new execution time (four-threaded and eight-threaded in this case)
"""

# The fairest comparison is between EVC-slow, SVT-3 and VVenc-medium
qps = [22, 27, 32, 37]
codecs = {"evc": "slow", "svt":"3", "vvcodec":"medium"}

def draw_plot(results: dict):
    groups = ['4', '8']
    fig, ax = plt.subplots()
    bar_width = 0.25
    opacity = 0.8
    index = range(len(groups))
    
    rects1 = ax.bar(index, results["vvcodec"].values(), bar_width, 
                alpha=opacity,
                label='vvcodec', color="#21c400")
    rects2 = ax.bar([i + 1*bar_width for i in index], results["evc"].values(), bar_width, 
                alpha=opacity,
                label='evc', color="#0003c4")
    rects3 = ax.bar([i + 2*bar_width for i in index], results["svt"].values(), bar_width, 
                alpha=opacity,
                label='svt', color="#c40000")

    # Set x-axis labels and fix the ticks, etc.
    plt.tick_params(axis='x', which='both', length=0, labelsize=14)
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(groups)
    ax.set_xlabel('Number of Threads', fontsize=14)
    ax.set_ylabel('Speedup (%)', fontsize=14)
    plt.title("Speedup vs Number of Threads", fontsize=16)

    ax.legend(fontsize=14)
    fig = plt.gcf()
    fig.set_size_inches(10, 6.5)
    fig.savefig('speedup.png', dpi=300)
    plt.show()   

def speedup(nthreads: list) -> dict:
    speedup = {} 
    for key, val in codecs.items():
        speedup[key] = {}
        for thread in nthreads:
            speedup[key][thread] = get_average_time(key, val, 1) / get_average_time(key, val, thread) * 100
    
    print("svt speedup:", speedup["svt"][4])
    print("svt calculation:",  get_average_time("svt", "3", 1), "/", get_average_time("svt", "3", 4))
    
    return speedup

def get_average_time(codec: str, preset: str, nthreads: int) -> float:
    path = f"output/{codec}/{preset}/csv"
    times = [] 

    for video_dir in os.listdir(path):
        for video in os.listdir(path + "/" + video_dir):
            for qp in qps:
                path50fps = f"{path}/{video_dir}/{video_dir}_{qp}qp_0fr_50fps_{preset}-preset_{nthreads}t.csv"
                path60fps = f"{path}/{video_dir}/{video_dir}_{qp}qp_0fr_60fps_{preset}-preset_{nthreads}t.csv"
                path30fps = f"{path}/{video_dir}/{video_dir}_{qp}qp_0fr_30fps_{preset}-preset_{nthreads}t.csv"
                
                real_path = ""
                if os.path.isfile(path50fps):
                    real_path = path50fps
                elif os.path.isfile(path60fps):
                    real_path = path60fps
                elif os.path.isfile(path30fps):
                    real_path = path30fps
                else:
                    raise FileNotFoundError(path30fps, path50fps, path60fps)

                with open(real_path, "r") as f:
                    times.append(get_individual_time(f.read())) 
                    f.close()

    return sum(times)/len(times)

def get_individual_time(contents: str) -> float:
    second_line = contents.split("\n")[1]
    comma_separated = second_line.split(',')
    time = comma_separated[11]
    return float(time)

draw_plot(speedup([4, 8]))

