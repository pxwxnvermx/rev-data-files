import argparse
import sys
import math
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

if not args.file:
    sys.exit()

with open(args.file, "rb") as f:
    RES = 256
    map = [[0] * RES for _ in range(RES)]
    pixels = [[0] * RES for _ in range(RES)]
    data = f.read()
    for i in range(len(data) - 1):
        x = int(data[i])
        y = int(data[i + 1])
        map[y][x] += 1

    mx = 0
    mn = 2**32
    for i in range(RES):
        for j in range(RES):
            if map[i][j]:
                f = math.log(map[i][j])
                mx = max(f, mx)
                mn = min(f, mn)

    image = Image.new(mode="L", size=(RES, RES))
    pix = image.load()
    for y in range(RES):
        for x in range(RES):
            val = map[y][x]
            val = math.log(val) if val else 0
            t = ((val - mn) * 255) / mx
            pixels[y][x] = int(t)
            pix[x, y] = pixels[y][x]
    image.save(f"{args.file}.out.png")
