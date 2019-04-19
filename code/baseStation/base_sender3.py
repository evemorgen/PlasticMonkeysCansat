# python2.7
# TODO: Argparse and pathlib

"""
Commands:

Image request:
"I" + 5-digit number + one of ['L', 'M', 'H', 'U']
Ex: I57743L
Requests transmission of image from given time (seconds since midnight)
at given quality (L - 120x160, M - 240x320, H - 480x640, U - 960x1280)

Thermal request:
"T" + 5-digit number
Ex: T35626
Requests transmission of thermal image from given time (seconds since midnight)

OLED Write:
"O" + string (max. 50 chars)
Clears OLED and writes the given string.

OLED Append:
"A" + string (max. 50 chars)
Appends string to OLED.
"""

while True:
    inp = input()
    with open("../../../tx.txt", "a") as tx:
        if len(inp) <= 11 and inp[0] not in "AO":  # Normal command
            tx.write(inp)
            tx.write("-"*(11-len(inp)))

        elif len(inp) > 11 and inp[0] not in "AO":
            print("Command too long!")

        else:  # OLED String parsing. Write it in one line
            split_string = [inp[i+1:i+11] for i in range(0, len(inp), 10)]
            tx.write(inp[0])
            tx.write(split_string[0])
            for chunk in split_string[1:]:
                tx.write("A")
                tx.write(chunk)
                tx.write("-"*(10-len(chunk)))
