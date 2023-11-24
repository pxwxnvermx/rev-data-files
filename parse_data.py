import argparse
import sys
import math
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-r", "--res")

args = parser.parse_args()

if not args.file:
    sys.exit()

RES = int(args.res) if args.res else 256
SCALE = RES / 256


def parse_blob(file: str) -> list[list[int]]:
    with open(file, "rb") as f:
        map = [[0] * RES for _ in range(RES)]
        pixels = [[0] * RES for _ in range(RES)]
        data = f.read()
        for i in range(len(data) - 1):
            x = int(data[i])
            y = int(data[i + 1])
            map[int(x * SCALE)][int(y * SCALE)] += 1

        mx = 0
        for x in range(RES):
            for y in range(RES):
                if map[x][y]:
                    f = math.log(map[x][y])
                    mx = max(f, mx)

        for x in range(RES):
            for y in range(RES):
                val = math.log(map[x][y]) if map[x][y] else 0
                t = (val * 255) / mx
                pixels[x][y] = int(t)

        return pixels


def save_image(file: str, pixels: list[list[int]]):
    image = Image.new(mode="L", size=(RES, RES))
    pix = image.load()
    for x in range(RES):
        for y in range(RES):
            pix[x, y] = pixels[x][y]
    image.save(f"{file}.out.png")


px = parse_blob(args.file)
save_image(args.file, px)
