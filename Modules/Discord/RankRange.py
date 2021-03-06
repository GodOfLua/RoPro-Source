
def getRankRange(string):
    f = string.split(":")
    if len(f) == 2:
        return {
            "min": int(f[0]),
            "max": int(f[1])
        }
    else:
        return {
            "min": int(f[0]),
            "max": int(f[0])
        }