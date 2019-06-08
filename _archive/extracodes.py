currX = 0
currY = 0
currP = 0

for event in dev.read_loop():
    if event.code == evdev.ecodes.ABS_MT_POSITION_X:
        currX = event.value
    if event.code == evdev.ecodes.ABS_MT_POSITION_Y:
        currY = event.value
    if event.code == evdev.ecodes.ABS_PRESSURE:
        currP = event.value

    print("({:>4}:{:>4}): {:>3}".format(currX, currY, currP), end="\r")


# Event: time 1559964153.776463, type 3 (EV_ABS), code 53 (ABS_MT_POSITION_X), value 1248
# Event: time 1559964153.776463, type 3 (EV_ABS), code 54 (ABS_MT_POSITION_Y), value 792
# Event: time 1559964153.776463, type 3 (EV_ABS), code 58 (ABS_MT_PRESSURE), value 98
# Event: time 1559964153.776463, type 3 (EV_ABS), code 0 (ABS_X), value 1248
# Event: time 1559964153.776463, type 3 (EV_ABS), code 1 (ABS_Y), value 792
# Event: time 1559964153.776463, type 3 (EV_ABS), code 24 (ABS_PRESSURE), value 98


# //////////////////////////////////////////////////////////////////////////////////////////////

## https://www.python-course.eu/tkinter_canvas.php

def paint(x, y, pressure):
    if pressure:
        python_green = "#476042"
        x1, y1 = ( x - scale * (pressure/maxP) ), ( y - scale * (pressure/maxP) )
        x2, y2 = ( x + scale * (pressure/maxP) ), ( y + scale * (pressure/maxP) )
        w.create_oval( x1, y1, x2, y2, fill = python_green )

def loopback(evt):
    print("Running Loopback")

    prevX = 0
    prevY = 0

    currX = 0
    currY = 0
    currP = 0

    for event in dev.read_loop():
        print("in loop")
        if event.code == evdev.ecodes.ABS_MT_POSITION_X:
            currX = event.value
        if event.code == evdev.ecodes.ABS_MT_POSITION_Y:
            currY = event.value
        if event.code == evdev.ecodes.ABS_PRESSURE:
            currP = event.value

        if currP and (currX != prevX or currY != prevY):
            prevX = currX
            prevY = currY

            print("painting ({:>4}:{:>4}): {:>3}".format(currX, currY, currP), end="\r")
            paint(currX, currY, currP)
master = Tk()
master.title( "Painting using Ovals" )
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", loopback )

message = Label( master, text = "Use your finger to draw" )
message.pack( side = BOTTOM )

mainloop()
