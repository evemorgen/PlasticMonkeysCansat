import serial

while True:
    inp = raw_input()
    with open("../../../tx.txt", "a") as tx:
        if len(inp) <= 11 and inp[0] not in "AO":
            tx.write(inp)
            tx.write("-"*(11-len(inp)))

        elif len(inp) > 11 and inp[0] not in "AO":
            print("Command too long!")

        else:
            split_string = [inp[i+1:i+11] for i in xrange(0, len(inp), 10)]
            tx.write(inp[0])
            tx.write(split_string[0])
            for chunk in split_string[1:]:
                tx.write("A")
                tx.write(chunk)
                tx.write("-"*(10-len(chunk)))
