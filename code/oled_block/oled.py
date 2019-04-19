import Adafruit_SSD1306
import time
import configparser

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

oled_buffer_path = config['SETTINGS']['oled_buffer_path'] # Path to oled buffer
line_width = config['SETTINGS']['line_width']  # Number of characters in one line
sleep_time = float(config['SETTINGS']['sleep_time']) # Delay between displaying in seconds

RST = 24 # Raspberry Pi RST pin, which we don't have to use xd

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST) # 128x64 display with hardware I2C:

disp.begin() # Initialize library.

width = disp.width #some useful constants
height = disp.height

font = ImageFont.load_default() # Load default font.

def get_message():
    with open(oled_buffer_path, 'r') as file:
        return file.read().replace('\n', '').replace('-','')

def write_message(message):
    disp.clear() #clear last message
    disp.display()
    y_pos = 0 #variable to store y axis position of line
    image = Image.new('1', (width, height)) #our graphic with text

    draw = ImageDraw.Draw(image) # Get drawing object to draw xd

    split_string = [message[i:i+line_width] for i in xrange(0, len(message), line_width)]
    for chunk in split_string[0:]:
        if len(chunk) == line_width and chunk[-1] != ' ':
            chunk = chunk + '-' # adds some swaggy hyphens when we split a word between two lines
        draw.text((0,y_pos), chunk, font=font, fill = 255)
        y_pos += 10

    # Display image.
    disp.image(image)
    disp.display()

while True:
    try:
        message = get_message()
        write_message(message)
        time.sleep(sleep_time)
    except Exception:
        sleep(0.2)
