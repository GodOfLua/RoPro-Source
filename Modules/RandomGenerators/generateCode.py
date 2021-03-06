
import random

def gen():
    code = ""
    for i in range(random.randint(4,7)):
        for i in range(random.randint(2,4)):
            code = code+'#'
        code = code+' '
    return code