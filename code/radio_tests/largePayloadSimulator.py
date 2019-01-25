f = open('tx.txt', 'w')

for i in range(500):
	line = str(i)
	line += "." * (20-len(line)) + "\n"
	f.write(line)

