#!/usr/bin/env python3

import evdev
import svgwrite

FILENAME        = "test.svg"
LINETHICKNESS   = 6

## Get input Device
dev = ""

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if "touchpad" in device.name.lower():
        dev = device
        # device.path, device.name, device.phys

print("Selected {} {} {}".format(dev.path, dev.name, dev.phys))



## Get Bounding box
print("")
print("Move your finger around your trackpad to the extremes to the bounding box. Press to get maximum pressure. ^C to Commit the maximum values")
print("Once you get the maximum value, take this time to set your cursor at a favourable position. Once you commit, the drawing will be captured.")
print("Saving to 'test.svg'")
print("")

maxX = 0
maxY = 0
maxP = 0

try:
    for event in dev.read_loop():
        if event.code == evdev.ecodes.ABS_MT_POSITION_X:
            if event.value > maxX: maxX = event.value
        if event.code == evdev.ecodes.ABS_MT_POSITION_Y:
            if event.value > maxY: maxY = event.value
        if event.code == evdev.ecodes.ABS_PRESSURE:
            if event.value > maxP: maxP = event.value

        print("({:>4}:{:>4}): {:>3}".format(maxX, maxY, maxP), end="\r")

except KeyboardInterrupt:
    print("\nBounding box set at ({}, {}), Max Pressure = {}".format(maxX, maxY, maxP))

prevX = 0
prevY = 0

currX = 0
currY = 0
currP = 0

linemode = False

lines = []
currLine = []
setMarker = 0

print("")
print("Capturing Drawing. All contact with the touchpad will be tracked. ^C to commit")

try:
    for event in dev.read_loop():
            if event.code == evdev.ecodes.ABS_MT_POSITION_X:
                setMarker += 1
                currX = event.value
            if event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                setMarker += 1
                currY = event.value
            if event.code == evdev.ecodes.ABS_PRESSURE:
                currP = event.value

            if not currP and linemode:
                lines.append(currLine)
                currLine = []
                linemode = False

            if currP and (currX != prevX or currY != prevY) and not setMarker % 2:
                linemode = True

                print("({:>4}:{:>4}) -> ({:>4}:{:>4}): {:>3} -- Paint".format(prevX, prevY, currX, currY, currP), end="\r")
                prevX = currX
                prevY = currY

                currLine.append((currX, currY, currP))

except KeyboardInterrupt:
    lines.append(currLine)
    pass

# save lines
print("============= Writing to {} =============".format(FILENAME))
dwg = svgwrite.Drawing(FILENAME, size=(str(maxX) + "px", str(maxY) + "px"))
for line in lines:
    if len(line):
        _d = []
        x = 0
        for pt in line:
            if not x:
                _d.append("M {},{}".format(pt[0], pt[1]))
                x = 1
            else:
                _d.append("L {},{}".format(pt[0], pt[1]))

        x = " ".join(_d).strip()
        # print(f">>{x}<<")
        dwg.add(dwg.path(d=x, stroke="#000", fill="none", stroke_width=LINETHICKNESS))
dwg.save()
