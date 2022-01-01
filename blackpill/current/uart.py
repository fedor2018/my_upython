from  grbl import *

g=grbl(debug=True)
g.req_parse(b'\x18' , 10) #
g.is_connect()
# 
g.req_parse(b"$I\r", 30) #build
g.req_parse(b"$\r", 10) #help
g.req_parse(b"$G\r", 10) #$G - View gcode parser state
g.req_parse(b"?", 10) #stat
# g.req_parse(b"$H\r", 1) #home
# g.req_parse(b"$X\r", 10) #kill alarm
g.req_parse(b"$$\r", 10) #check mode

g.disconnect()
     