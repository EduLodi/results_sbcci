import pandas as pd
import matplotlib.pyplot as plt
import os

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


psnrlist = []
bitratelist = []
timelist = []
vmaflist = []

mode = "BRxTIME"

videoarray = ["icecif", "ice4cif", "harbourcif", "harbour4cif", "duckstakeoff720p", "duckstakeoff1080p", "duckstakeoff2160p", "parkjoy720p", "parkjoy1080p", "parkjoy2160p"]

for thread in ["1t", "4t", "8t"]:

    for video in videoarray:

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

                for qp in ["17qp","22qp","27qp","32qp","37qp","42qp"]:
                    
                    #df = pd.read_csv(csv_path_vmaf)
                    #mask = (df['name'].str.contains(qp)) & (df['name'].str.contains("_"+preset+"-preset"))
                    #result = df[mask]
                    #vmaflist.append(result["avg_vmaf"].tolist()[0])

                        for filename in os.listdir(folder_path_csv):
                            if thread in filename:    
                                if qp in filename:
                                    df = pd.read_csv(os.path.join(folder_path_csv, filename))
                                    print(os.path.join(folder_path_csv, filename))
                                    psnrlist.append(df.at[0, 'psnr'])
                                    bitratelist.append(df.at[0, 'bitrate'])
                                    timelist.append(df.at[0, "time(s)"])




                color = color_dict[codec+preset]
                if mode == "PSNRxBR":
                    plt.plot(bitratelist, psnrlist, "o-", label=codec+preset, color = color, markersize = 5)
                if mode == "PSNRxTIME":
                    plt.plot(timelist, psnrlist, "o-", label=codec+preset, color = color, markersize = 5)    
                if mode == "BRxTIME":
                    plt.plot(timelist, bitratelist, "o-", label=codec+preset, color = color, markersize = 5)
                if mode == "VMAFxTIME":
                    plt.plot(timelist, vmaflist, "o-", label=codec+preset, color = color, markersize = 5)
                if mode == "VMAFxBR":
                    plt.plot(bitratelist,vmaflist, "o-", label=codec+preset, color = color, markersize = 5)

                psnrlist = []
                bitratelist = []
                vmaflist = []
                timelist = []


        if mode == "PSNRxBR":
            plt.xlabel('Bitrate')
            plt.ylabel('PSNR')
            plt.title(video + " " + thread + ' PNSR vs Bitrate')
        if mode == "BRxTIME":
            plt.xlabel('Time(s)')
            plt.ylabel('Bitrate')
            plt.title(video + " " + thread + ' PNSR vs Bitrate')
        if mode == "PSNRxTIME":
            plt.xlabel('Time(s)')
            plt.ylabel('PSNR')
            plt.title(video + " " + thread + ' PNSR vs Bitrate')    
        if mode == "VMAFxTIME":
            plt.xlabel('Time(s)')
            plt.ylabel('VMAF score')
            plt.title(video + ' VMAF vs Time')
        if mode == "VMAFxBR":
            plt.xlabel('Bitrate')
            plt.ylabel('VMAF score')
            plt.title(video + ' VMAF vs Bitrate')

        plt.legend()
        plt.grid()
        plt.show()
    
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