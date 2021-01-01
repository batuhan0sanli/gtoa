import time, sys

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress, num):
    barLength = 40 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text1 = '\rhi'
    text = "\rhiPercent: [{0}] {1}% {2} {3}".format( "#"*block + "-"*(barLength-block), progress*100, status, num)
    sys.stdout.write(text)
    sys.stdout.flush()


"""
print("")
print("Deneme")
for i in range(1,10+1):
    time.sleep(0.4)
    update_progress(i/10, i)

print("")
print("Test completed")
"""

"""
from tqdm import tqdm, trange
num = 100

a = trange(num, desc='Bar desc', leave=True)
for i in a:
#    a.set_description(str(i))
    a.refresh()
    time.sleep(0.6)
"""

from utilities import fixLength

no = 12345.454545
no = fixLength(no, 6)
print(no)
