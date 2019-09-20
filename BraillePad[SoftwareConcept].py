#CSUN AI JAM 2019 - SARKIS MIKAELIAN [Braille Pad]
# Using utf-8

from PIL import Image
import codecs
import sys

def get_char(current):
    if current != [0,0,0,0,0,0,0,0]:
        total_val = current[0] + (current[1] << 1) + (current[2] << 2) + (current[4] << 3) + (current[5] << 4) + (current[6] << 5) + (current[3] << 6) +(current[7] << 7)
    else:
        total_val = 4
    return unichr(0x2800 + total_val)

def nearest_multiple(num, mult):
    return num - (num%mult)

try:
    im = Image.open(sys.argv[1])
except IndexError:
    print "Use file as an argument, drag file into script: "
    raise SystemExit

#Removing alpha channel RGB.
try:
	bg = Image.new("RGB", im.size, (255, 255, 255))
	bg.paste(im, mask=im.split()[3]) # 3 is the alpha channel
	im = bg
except:
	pass
	
#Resiing imgage for convenience.

width = im.size[0]
height = im.size[1]
if width > 100:
    height = 100 * height / width
    width = 100

width = nearest_multiple(width, 2)
height = nearest_multiple(height, 4)
im = im.resize(( width, height ), Image.NEAREST)

try:
    weight = float(sys.argv[2])
except IndexError:
    weight = 3
    
px = im.load()
output = u""

for imgy in range(0, height, 4):
    for imgi in range(0, width, 2):    
        current = [0,0,0,0,0,0,0,0]
        cindex = 0
        for x in range(2):
            for y in range(4):
                temp = px[imgi+x, imgy+y]
                avg = (temp[0] + temp[1] + temp[2]) / weight
                if(avg < 128):
                    current[cindex] = 1
                cindex += 1
    
        output += get_char(current)
    output += u"\r\n"

#Printing the output.

with codecs.open("braille.txt", "w", "utf-8-sig") as b:
    b.write(output)
