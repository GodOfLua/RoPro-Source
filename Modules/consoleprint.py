from colorama import Fore,Back,Style
import time
def getTime(start_time):
    Time = round(time.time()-start_time,3)
    if len(str(Time).split(".")[1]) == 2:
        Time = str(Time)+"0"
    elif len(str(Time).split(".")[1]) == 1:
        Time = str(Time)+"00"
    return Time

def printi(msg,start_time):
    print(f"{Fore.LIGHTBLACK_EX}{str(getTime(start_time))} | {Style.RESET_ALL}{msg}")