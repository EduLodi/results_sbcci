import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
import numpy as np

from CodecComparator import CodecComparator

presetsvvenc8t = ["faster","fast","medium","slow"]
presetssvt8t = ["0","3","6","9","12"]
presetsevc8t = ["fast","medium","slow","placebo"]

presetsvvenc4t = ["faster","fast","medium","slow"]
presetssvt4t = ["3","6","9","12"]
presetsevc4t = ["fast","medium","slow","placebo"]

presetsvvenc1t = ["faster","fast","medium"]
presetssvt1t = ["3","6","9","12"]
presetsevc1t = ["fast","medium","slow","placebo"]

color_dict = {
    "svt0": "#660000",
    "svt1": "#CC0000",
    "svt2": "#FF6666",
    "svt3": "#663300",
    "svt4": "#CC6600",
    "svt5": "#FF9933",
    "svt6": "#FFCC99",
    "svt7": "#666600",
    "svt8": "#FFFF00",
    "svt9": "#006600",
    "svt10": "#00CC00",
    "svt11": "#66FF66",
    "svt12": "#CCFFE5",
    "vvcodecfaster": "#009999",
    "vvcodecfast": "#33FFFF",
    "vvcodecmedium": "#000099",
    "vvcodecslow": "#4C0099",
    "vvcodecslower": "#9933FF",
    "evcfast": "#CC00CC",
    "evcmedium": "#FF66FF",
    "evcslow": "#99004C",
    "evcplacebo": "#606060",
}

color_dict = {
    "svt3": "#c40000",
    "svt6": "#c40000",
    "svt9": "#c40000",
    "svt12": "#c40000",
    "vvcodecfaster": "#21c400",
    "vvcodecfast": "#21c400",
    "vvcodecmedium": "#21c400",
    "evcfast": "#0003c4",
    "evcmedium": "#0003c4",
    "evcslow": "#0003c4",
    "evcplacebo": "#0003c4",
}

marker_dict = {
    "svt3": "^",
    "svt6": "v",
    "svt9": "^",
    "svt12": "v",
    "vvcodecfaster": "o",
    "vvcodecfast": "s",
    "vvcodecmedium": "o",
    "evcfast": "<",
    "evcmedium": ">",
    "evcslow": "<",
    "evcplacebo": ">",
}

markstyle_dict = {
    "svt3": "full",
    "svt6": "full",
    "svt9": "none",
    "svt12": "none",
    "vvcodecfaster": "none",
    "vvcodecfast": "none",
    "vvcodecmedium": "full",
    "evcfast": "none",
    "evcmedium": "none",
    "evcslow": "full",
    "evcplacebo": "full",
}


def baseline_list(codecname, videoname, metric):
    # Define dictionary with codec and video names as keys, and corresponding lists as values
    codec_video_dict = {
        ("vvcodec","icecif","bitrate"): [727190.528, 362350.592, 192218.112, 107209.728] ,
        ("vvcodec","icecif","psnr"): [46.9683, 43.4699, 40.0982, 36.9726] ,
        ("vvcodec","ice4cif","bitrate"): [3166971.904, 1159593.984, 531959.808, 278302.72] ,
        ("vvcodec","ice4cif","psnr"): [45.6675, 43.3623, 40.9889, 38.5962] ,
        ("vvcodec","harbourcif","bitrate"): [1337489.8176, 609258.7008, 265990.144, 123230.6176] ,
        ("vvcodec","harbourcif","psnr"): [38.9481, 35.6, 32.6099, 30.2122] ,
        ("vvcodec","harbour4cif","bitrate"): [8075815.3216, 3143208.1408, 1331169.6896, 616856.7808] ,
        ("vvcodec","harbour4cif","psnr"): [40.2989, 37.5237, 35.0531, 32.8381] ,
        ("vvcodec","duckstakeoff720p","bitrate"): [29805701.5296, 10797395.1488, 4124372.992, 1686014.3616] ,
        ("vvcodec","duckstakeoff720p","psnr"): [36.2287, 32.4808, 29.7488, 27.6533] ,
        ("vvcodec","duckstakeoff1080p","bitrate"): [63115795.6608, 19868524.544, 7250622.0544, 2884089.4464] ,
        ("vvcodec","duckstakeoff1080p","psnr"): [35.6887, 32.528, 30.1386, 28.1981] ,
        ("vvcodec","duckstakeoff2160p","bitrate"): [265424645.3248, 48342090.5472, 15735205.0688, 6392722.2272] ,
        ("vvcodec","duckstakeoff2160p","psnr"): [34.3212, 31.9036, 30.6213, 29.2868] ,
        ("vvcodec","parkjoy720p","bitrate"): [18337358.6432, 7681733.4272, 3093372.1088, 1229819.0848] ,
        ("vvcodec","parkjoy720p","psnr"): [35.0248, 31.4729, 28.4818, 26.1014] ,
        ("vvcodec","parkjoy1080p","bitrate"): [34663750.8608, 14162034.688, 5548389.9904, 2215502.6432] ,
        ("vvcodec","parkjoy1080p","psnr"): [35.4028, 32.089, 29.2126, 26.9204] ,
        ("vvcodec","parkjoy2160p","bitrate"): [70836982.5792, 28791624.4992, 11649017.4464, 4856461.7216] ,
        ("vvcodec","parkjoy2160p","psnr"): [36.2686, 34.1175, 31.7909, 29.6272] ,
        ("evc","icecif","bitrate"): [576568.32, 292905.984, 158708.736, 86924.288] ,
        ("evc","icecif","psnr"): [43.3717, 39.8224, 36.8859, 34.2036] ,
        ("evc","ice4cif","bitrate"): [2087734.272, 954927.104, 500894.72, 270683.136] ,
        ("evc","ice4cif","psnr"): [43.8201, 41.3726, 39.1092, 36.7659] ,
        ("evc","harbourcif","bitrate"): [1643282.432, 624069.8368, 248369.9712, 96517.3248] ,
        ("evc","harbourcif","psnr"): [38.8706, 35.1345, 32.3728, 30.0745] ,
        ("evc","harbour4cif","bitrate"): [8505440.6656, 2856333.312, 1154031.616, 468562.7392] ,
        ("evc","harbour4cif","psnr"): [39.9076, 36.8459, 34.4697, 32.1926] ,
        ("evc","duckstakeoff720p","bitrate"): [42629201.92, 16264867.0208, 6492803.072, 2510621.9008] ,
        ("evc","duckstakeoff720p","psnr"): [36.7911, 33.0203, 30.4095, 28.2446] ,
        ("evc","duckstakeoff1080p","bitrate"): [95900976.7424, 32610745.5488, 12726935.552, 4933585.3056] ,
        ("evc","duckstakeoff1080p","psnr"): [36.2436, 33.0097, 30.7702, 28.8403] ,
        ("evc","duckstakeoff2160p","bitrate"): [467314223.5136, 97486935.6544, 31631229.7472, 13442486.272] ,
        ("evc","duckstakeoff2160p","psnr"): [35.4554, 32.2463, 31.073, 29.8705] ,
        ("evc","parkjoy720p","bitrate"): [37466099.712, 15097083.4944, 6352027.648, 2446330.2656] ,
        ("evc","parkjoy720p","psnr"): [36.9685, 32.7517, 29.8518, 27.4184] ,
        ("evc","parkjoy1080p","bitrate"): [73260928.2048, 29256412.3648, 12274248.9088, 4839632.896] ,
        ("evc","parkjoy1080p","psnr"): [37.1292, 33.2858, 30.5056, 28.1429] ,
        ("evc","parkjoy2160p","bitrate"): [183618585.3952, 63464698.6752, 27505357.6192, 12059389.952] ,
        ("evc","parkjoy2160p","psnr"): [37.4008, 34.8886, 32.7601, 30.6935] ,
        ("svt","icecif","bitrate"): [538644.48, 433909.76, 337530.88, 259747.84] ,
        ("svt","icecif","psnr"): [46.24, 45.13, 43.85, 42.52] ,
        ("svt","ice4cif","bitrate"): [2480046.08, 1798164.48, 1317437.44, 963287.04] ,
        ("svt","ice4cif","psnr"): [46.1, 45.36, 44.57, 43.7] ,
        ("svt","harbourcif","bitrate"): [1892259.84, 1364705.28, 955074.56, 655943.68] ,
        ("svt","harbourcif","psnr"): [41.2, 39.8, 38.43, 37.13] ,
        ("svt","harbour4cif","bitrate"): [11276564.48, 7566018.56, 4829153.28, 3129057.28] ,
        ("svt","harbour4cif","psnr"): [41.85, 40.66, 39.49, 38.41] ,
        ("svt","duckstakeoff720p","bitrate"): [52453468.16, 36496711.68, 25128284.16, 16632832.0] ,
        ("svt","duckstakeoff720p","psnr"): [38.92, 37.27, 35.77, 34.3] ,
        ("svt","duckstakeoff1080p","bitrate"): [128529602.56, 82443796.48, 52842526.72, 33534832.64] ,
        ("svt","duckstakeoff1080p","psnr"): [38.46, 36.7, 35.35, 34.11] ,
        ("svt","duckstakeoff2160p","bitrate"): [686617108.48, 431365273.6, 238725642.24, 109476239.36] ,
        ("svt","duckstakeoff2160p","psnr"): [38.19, 35.98, 34.25, 32.94] ,
        ("svt","parkjoy720p","bitrate"): [41975142.4, 31740938.24, 22450452.48, 15673845.76] ,
        ("svt","parkjoy720p","psnr"): [39.53, 37.98, 36.23, 34.62] ,
        ("svt","parkjoy1080p","bitrate"): [85469358.08, 62882570.24, 43853557.76, 30346905.6] ,
        ("svt","parkjoy1080p","psnr"): [39.36, 38.0, 36.49, 35.02] ,
        ("svt","parkjoy2160p","bitrate"): [257051463.68, 159863398.4, 97251061.76, 64592599.04] ,
        ("svt","parkjoy2160p","psnr"): [39.14, 37.98, 36.95, 36.06]
    }

    # Get the corresponding list from the dictionary based on input codec and video names
    try:
        list_to_return = codec_video_dict[(codecname, videoname, metric)]
    except KeyError:
        print("Invalid codec or video name.")
        return None

    return list_to_return

def heatplot(videoname, threads, codeclist, timelist, bdratelist, bdpsnrlist, basecodec):
    # Create a dictionary with your data
    data = {'codec_config': codeclist,
            'time': timelist,
            'bdrate': bdratelist,
            'bdpsnr': bdpsnrlist}
    pathtoresults = os.path.join(os.path.expanduser("~"),"videocoding","results_sbcci","initialresultssbcci")
    threadpath = thread+"hread"
    if "EVC" in basecodec:
        basecodecpath = "vsEVC"
    if "VVenC" in basecodec:
        basecodecpath = "vsVVCODEC"
    if "SVT" in basecodec:
        basecodecpath = "vsSVT"
    figname = videoname+".png"
    fullsavepath = os.path.join(pathtoresults,threadpath,"heatBDRATE",basecodecpath,figname)

    # Convert the dictionary to a Pandas DataFrame
    df = pd.DataFrame.from_dict(data)

    # Reshape the DataFrame to a pivot table format
    table = df.pivot(index='time', columns='codec_config', values='bdrate')

    # Create a heatmap with seaborn
    plt.figure(figsize=(13, 7))
    ax = sns.heatmap(table, cmap='coolwarm', annot=True, fmt=".2f")

    # Add labels for the x and y axes
    ax.set_xlabel('Codec and preset')
    ax.set_ylabel('Time (s)')
    ax.set_title("Heatmap of BD-rate(%) and time for "+videoname+" encoded with " + threads[:-1] + " threads")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    plt.suptitle("Using "+basecodec+" as baseline for BD-rate calculation")
    # Show the plot
    plt.savefig(fullsavepath ,dpi=200)

    fullsavepath = os.path.join(pathtoresults,threadpath,"heatBDPSNR",basecodecpath,figname)

    table = df.pivot(index='time', columns='codec_config', values='bdpsnr')

    # Create a heatmap with seaborn
    plt.figure(figsize=(13, 7))
    ax = sns.heatmap(table, cmap='coolwarm', annot=True, fmt=".2f")

    # Add labels for the x and y axes
    ax.set_xlabel('Codec and preset')
    ax.set_ylabel('Time (s)')
    ax.set_title("Heatmap of BD-PSNR(dB) and time for "+videoname+" encoded with " + threads[:-1] + " threads")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    plt.suptitle("Using "+basecodec+" as baseline for BD-PSNR calculation")
    # Show the plot
    plt.savefig(fullsavepath,dpi=200)

psnrlist = []
bitratelist = []
timelist = []
vmaflist = []

codecconfig = []
timeconfig = []
bdratesvt = []
bdpsnrsvt = []
bdratevvcodec = []
bdpsnrvvcodec = []
bdrateevc = []
bdpsnrevc = []

comp = CodecComparator()

mode = "PSNRxBR"

videoarray = ["icecif", "ice4cif", "harbourcif", "harbour4cif", "duckstakeoff720p", "duckstakeoff1080p", "duckstakeoff2160p", "parkjoy720p", "parkjoy1080p", "parkjoy2160p"]

for thread in ["1t"]:

    for video in videoarray:
        fig = plt.figure(figsize=(12, 9))
        for codec in ["svt","evc","vvcodec"]:

            if codec == "svt" and thread == "1t":
                presets = presetssvt1t
            if codec == "vvcodec" and thread == "1t":
                presets = presetsvvenc1t
            if codec == "evc" and thread == "1t":
                presets = presetsevc1t

            if codec == "svt" and thread == "4t":
                presets = presetssvt4t
            if codec == "vvcodec" and thread == "4t":
                presets = presetsvvenc4t
            if codec == "evc" and thread == "4t":
                presets = presetsevc4t

            if codec == "svt" and thread == "8t":
                presets = presetssvt8t
            if codec == "vvcodec" and thread == "8t":
                presets = presetsvvenc8t
            if codec == "evc" and thread == "8t":
                presets = presetsevc8t        

            for preset in presets:

                folder_path_csv = os.path.join("output",codec,preset,"csv",video)
                #csv_path_vmaf = os.path.join("output",codec,"metrics","VMAF",video,"averageVMAFs","pathavg_vmaf.csv")

                for qp in ["22qp","27qp","32qp","37qp"]:
                    
                    #df = pd.read_csv(csv_path_vmaf)
                    #mask = (df['name'].str.contains(qp)) & (df['name'].str.contains("_"+preset+"-preset"))
                    #result = df[mask]
                    #vmaflist.append(result["avg_vmaf"].tolist()[0])

                        for filename in os.listdir(folder_path_csv):
                            if thread in filename:    
                                if qp in filename:
                                    df = pd.read_csv(os.path.join(folder_path_csv, filename))
                                    #print(os.path.join(folder_path_csv, filename))
                                    psnrlist.append(df.at[0, 'psnr'])
                                    bitratelist.append(df.at[0, 'bitrate'])
                                    timelist.append(df.at[0, "time(s)"])
                                
                avg_time = (timelist[0] + timelist[1] + timelist[2] + timelist[3]) / 4
                
                timeconfig.append(avg_time)
                codecconfig.append((codec+"_"+preset))
                
                #print("BDRATE for "+video+" encoded with "+codec+" at preset "+preset+" with SVT0 as baseline: ")
                brbaselist = baseline_list("svt",video,"bitrate")
                psnrbaselist = baseline_list("svt",video,"psnr")
                bdratesvt.append(comp.BD_RATE(brbaselist,psnrbaselist,bitratelist,psnrlist))
                #print("BDPSNR for "+video+" encoded with "+codec+" at preset "+preset+" with SVT0 as baseline: ")
                brbaselist = baseline_list("svt",video,"bitrate")
                psnrbaselist = baseline_list("svt",video,"psnr")
                bdpsnrsvt.append(comp.BD_PSNR(brbaselist,psnrbaselist,bitratelist,psnrlist))

                #print("BDRATE for "+video+" encoded with "+codec+" at preset "+preset+" with vvcodec slow as baseline: ")
                brbaselist = baseline_list("vvcodec",video,"bitrate")
                psnrbaselist = baseline_list("vvcodec",video,"psnr")
                bdratevvcodec.append(comp.BD_RATE(brbaselist,psnrbaselist,bitratelist,psnrlist))
                #print("BDPSNR for "+video+" encoded with "+codec+" at preset "+preset+" with vvcodec slow as baseline: ")
                brbaselist = baseline_list("vvcodec",video,"bitrate")
                psnrbaselist = baseline_list("vvcodec",video,"psnr")
                bdpsnrvvcodec.append(comp.BD_PSNR(brbaselist,psnrbaselist,bitratelist,psnrlist))

                #print("BDRATE for "+video+" encoded with "+codec+" at preset "+preset+" with evc slow as baseline: ")
                brbaselist = baseline_list("evc",video,"bitrate")
                psnrbaselist = baseline_list("evc",video,"psnr")
                bdrateevc.append(comp.BD_RATE(brbaselist,psnrbaselist,bitratelist,psnrlist))
                #print("BDPSNR for "+video+" encoded with "+codec+" at preset "+preset+" with evc slow as baseline: ")
                brbaselist = baseline_list("evc",video,"bitrate")
                psnrbaselist = baseline_list("evc",video,"psnr")
                bdpsnrevc.append(comp.BD_PSNR(brbaselist,psnrbaselist,bitratelist,psnrlist))               
                   
                if video in ["icecif", "ice4cif", "harbourcif", "harbour4cif"]:    
                    bitratelist = [np.log10(i/1000) for i in bitratelist]
                else:
                    bitratelist = [np.log10(i/1000000) for i in bitratelist]
                color = color_dict[codec+preset]
                marker = marker_dict[codec+preset]
                markerstyle = markstyle_dict[codec+preset]
                if mode == "PSNRxBR":
                    bitratelist = [np.log2(br) for br in bitratelist]
                    plt.plot(bitratelist, psnrlist, "o", label=codec+preset, linewidth = 3, color=color, markersize=14, marker=marker, fillstyle=markerstyle)
                #if mode == "PSNRxTIME":
                #    plt.plot(timelist, psnrlist, "o-", label=codec+preset, color = color, markersize = 5)    
                #if mode == "BRxTIME":
                #    plt.plot(timelist, bitratelist, "o-", label=codec+preset, color = color, markersize = 5)
                #if mode == "VMAFxTIME":
                #    plt.plot(timelist, vmaflist, "o-", label=codec+preset, color = color, markersize = 5)
                #if mode == "VMAFxBR":
                #    plt.plot(bitratelist,vmaflist, "o-", label=codec+preset, color = color, markersize = 5)

                psnrlist = []
                bitratelist = []
                vmaflist = []
                timelist = []
                
        timeconfig = [round(value,2) for value in timeconfig]
        #heatplot(video, thread, codecconfig, timeconfig, bdratesvt, bdpsnrsvt,"SVT 0 with 8 threads")
        #heatplot(video,thread, codecconfig, timeconfig, bdratevvcodec, bdpsnrvvcodec,"VVenC slow with 8 threads")
        #heatplot(video, thread, codecconfig, timeconfig, bdrateevc, bdpsnrevc, "EVC slow with 8 threads")
        codecconfig=[]
        timeconfig=[]
        bdratesvt = []
        bdpsnrsvt = []
        bdratevvcodec = []
        bdpsnrvvcodec = []
        bdrateevc = []
        bdpsnrevc = []
        if mode == "PSNRxBR":
            if video in ["icecif", "ice4cif", "harbourcif", "harbour4cif"]:
                plt.xlabel('Bitrate (Kbps) [logarithmic]', fontsize=16)
            else:
                plt.xlabel('Bitrate (Mbps) [logarithmic]', fontsize=16)
            plt.ylabel('PSNR (dB)', fontsize=14)
            plt.title(video + " encoded with " + thread + 'hread PNSR vs Bitrate', fontsize=20)
        #if mode == "BRxTIME":
        #    plt.xlabel('Time(s)')
        #    plt.ylabel('Bitrate')
        #    plt.title(video + " " + thread + ' PNSR vs Bitrate')
        #if mode == "PSNRxTIME":
        #    plt.xlabel('Time(s)')
        #    plt.ylabel('PSNR')
        #    plt.title(video + " " + thread + ' PNSR vs Bitrate')    
        #if mode == "VMAFxTIME":
        #    plt.xlabel('Time(s)')
        #    plt.ylabel('VMAF score')
        #    plt.title(video + ' VMAF vs Time')
        #if mode == "VMAFxBR":
        #    plt.xlabel('Bitrate')
        #    plt.ylabel('VMAF score')
        #    plt.title(video + ' VMAF vs Bitrate')

        plt.legend(fontsize=14, loc='lower right')
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.grid()
        #plt.show()
        plt.savefig('initialresultssbcci/1thread/PSNRxBR/'+video+'.pdf', dpi=200, bbox_inches='tight')
    
    psnrlist = []
    bitratelist = []
    timelist = []
    vmaflist = []
#                        if qp == "22qp":                        
#                            timelist22qp.append(time_ms)
#                        else:
#                            if qp == "27qp":
#                                timelist27qp.append(time_ms)
#                            else:
#                                if qp == "32qp":
#                                    timelist32qp.append(time_ms)
#                                else:
#                                    if qp == "37qp":
#                                        timelist37qp.append(time_ms)
#                if qp == "22qp":                        
#                    vmaflist22qp.append(vmaf)
#                else: 
#                    if qp == "27qp":
#                        vmaflist27qp.append(vmaf)
#                    else:
#                        if qp == "32qp":
#                            vmaflist32qp.append(vmaf)
#                        else: 
#                            if qp == "37qp":
#                                vmaflist37qp.append(vmaf)
