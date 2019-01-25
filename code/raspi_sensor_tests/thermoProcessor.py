import argparse

IMAGE_WIDTH = 24
IMAGE_HEIGHT = 32

def getLineValues():
	line = f.readline()
	position = 1
	valList = []
	
	for x in range(IMAGE_WIDTH):
		valList.append(float(line[position:position+5]))
		position += 7
	return valList

def average2d(arr):
	s = 0
	for row in arr:
		s += sum(row)
	return s/len(arr)/len(arr[0])


parser = argparse.ArgumentParser(description="Thermal image processor")
parser.add_argument("--minimal-difference", "-d", type=float, default=4)
parser.add_argument("--skip", "-s", type=int, default=6)
parser.add_argument("--count", "-c", type=int, default=1)
parser.add_argument("--file", "-f")
args = parser.parse_args()

SKIP = args.skip
DET = args.minimal_difference

f = open(args.file)

for _ in range((IMAGE_HEIGHT+1)*SKIP+4):
	f.readline()

for img in range(args.count):
	print("---- IMAGE {} ----".format(img+1))
	image = []
	for y in range(IMAGE_HEIGHT):
		image.append(getLineValues())

	avg = average2d(image)
	print("Avg temp: {:.2f}".format(avg))

	for y in range(IMAGE_HEIGHT):
		for x in range(IMAGE_WIDTH):
			val = image[y][x]
			if val > avg + DET:
				print("[{:2d}, {:2d}] Val: {:4.1f} Diff: {:4.1f}".format(x, y, val, val-avg))
	
	if len(f.readline()) == 0:
		break
