import time
from PCD8544 import PCD8544
import lcd_gfx
# import network
import bmp
d = PCD8544()
d.reset()
d.begin()
time.sleep(5)
d.clear()
d.display()
d.p_string('The quick brown fox jumped over the lazy dog')
d.display()
time.sleep(5)
d.clear()
lcd_gfx.drawTrie(42,2,21,23,63,23,d,1)
d.display()
time.sleep(1)
lcd_gfx.drawFillRect(10,12,20,20,d,1)
d.display()
time.sleep(1)
lcd_gfx.drawCircle(70,24,10,d,1)
d.display()
time.sleep(1)

d.clear()
bmp.bmp('icon.bmp',d)
d.display()
time.sleep(5)




