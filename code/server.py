import random
import string
import time
def getRandom():
    return '"' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(22)) + '"'
result=0
for i in range(100):
    start=time.time()
    print(getRandom())
    over=time.time()
    result=result+over-start
print(str(result/100))
