# Author: peppe8o
# Blog: https://peppe8o.com
# Date: Aug 17th, 2021
# Version: 1.0

from machine import Pin
import utime

# define PINs according to cabling
# following array matches 1,2,3,4 PINs from 4x4 Keypad Matrix
col_list=["B5", "B4", "B3", "A15"] #[1,2,3,4]
# following array matches 5,6,7,8 PINs from 4x4 Keypad Matrix
row_list=["A0", "A1", "A2", "A3"] #[5,6,7,8]

# set row pins to output and change array elements from
#    int to Pin objects, all set to high
for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)

# set columns pins to input and change array elements 
#   from int to Pin objects. We'll read user input here
for x in range(0,4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)

# Create a map between keypad buttons and chars
key_map=[["D","#","0","*"],\
         ["C","9","8","7"],\
         ["B","6","5","4"],\
         ["A","3","2","1"]]

def Keypad4x4Read(cols,rows):
  for r in rows:
    r.value(0)
    result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
    if min(result)==0:
      key=key_map[int(rows.index(r))][int(result.index(0))]
      r.value(1) # manages key keept pressed
      return(key)
    r.value(1)

# Start the main loop
print("--- Ready to get user inputs ---")
while True:
    key=Keypad4x4Read(col_list, row_list)
    if key != None:
      print("You pressed: "+key)
      utime.sleep(0.3) # gives user enoght time to release without having double inputs


