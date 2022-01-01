# stm32f4_lpt
stm32f411 black + lpt

# Lathe-CNC-GRBL

```
  01234567890123456789|
0 M: x.xxmm RPM: xxxx |
0 T: x.xxbpi RPM: xxxx|
0 F: x.xxmm RPM: xxxx |
1 ????     |
2 Z:-zzz.zz X:-xxx.xx | 
3 -xxx.xx SSSS -yyy.yy|

SSSS:
```
Idle
Run
Hold
Door
Home
Alarm
Check
Jog
Sleep
Tool

```

```
$10=0 #Wpos only
?
<Idle|WPos:-20.000,0.000,0.000|Bf:15,128|FS:0,0|WCO:20.000,0.000,0.000>
<Idle|WPos:-20.000,0.000,0.000|Bf:15,128|FS:0,0|Ov:100,100,100>
<Idle|MPos:0.000,0.000,0.000|Bf:35,1024|FS:0,0,0|Pn:Y|WCO:0.000,0.000,0.000|Ov:100,100,100|A:M>
$J=G21G91X-0.1F1000
$J=G21G91X0.1F1000
G4P0 - stop streaming
$X - Kill alarm lock
G95 - mm/r

```

## display
```
01234567890123456789
STATUS: 0000
POS: X    MPG: 9999
S: 9999  F: 9999
O:  999  O:  999
     MC       WC
X - 999.99 - 999.99
Y - 999.99 - 999.99
X - 999.99 - 999.99
```

## lathe
```
01234567890123456789|
  Thread: x.xxmm    |
  Thread: x.xxbpi   |
    Feed: x.xxmm    |
  CCW Ang xxx.x     |
  ACW RPM  xxxx     |
    << -zzz.zz >>   | 
-xxx.xx SSSS -yyy.yy|

SSSS:
    RUN
    WAIT
    END
    STOP
    ACCEL
    DECEL
    FAST
```


