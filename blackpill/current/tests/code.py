print("Hello World!")
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode
import time

t1=time.monotonic_ns()
lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27))
print((time.monotonic_ns()-t1)/1000000)

lcd.print("abc ")
lcd.print("This is quite long and will wrap onto the next line automatically.")
print((time.monotonic_ns()-t1)/1000000)
# time.sleep(3)
lcd.clear()

# Start at the second line, fifth column (numbering from zero).
lcd.set_cursor_pos(1, 4)
lcd.print("Here I am")

# Make the cursor visible as a line.
lcd.set_cursor_mode(CursorMode.LINE)
print((time.monotonic_ns()-t1)/1000000)

print("END")
"""Hello World!
25.8484
287.506
330.78
END"""
