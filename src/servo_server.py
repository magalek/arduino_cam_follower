from time import sleep
import serial
import PySimpleGUI as sg
import socket
from enum import Enum

class Side(Enum):
    Left = 1
    Right = 2
    Center = 3

THRESHOLD = 0.05

last_side = Side.Center

started = False

offset = (0,0)

def write_to_motor(side):
    if (side == Side.Left): ser.write(bytes(LEFT))
    if (side == Side.Right): ser.write(bytes(RIGHT))
    if (side == Side.Center): ser.write(bytes(HOLD))

def try_move(offset):

    global last_side

    if (not started):
        return

    offset_split = offset.split(',')

    x = float(offset_split[0])
    y = float(offset_split[1])

    if (x < THRESHOLD and x > -THRESHOLD and last_side is not Side.Center):
        last_side = Side.Center
        write_to_motor(last_side)
        return
    if (x > THRESHOLD and last_side is not Side.Right):
        last_side = Side.Right
        write_to_motor(last_side)
        return
    if (x < -THRESHOLD and last_side is not Side.Left):
        last_side = Side.Left
        write_to_motor(last_side)
        return

LEFT = b'1'
RIGHT = b'2'
HOLD = b'3'

layout = [[sg.Text("Offset:", key="offset_label")], [sg.Button("Start")]]

window = sg.Window("Demo", layout, size=(200, 200))

ser = serial.Serial('COM12', 115200)

s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)
c, addr = s.accept()
while True:
    event, values = window.read(10)
    rcvdData = c.recv(1024).decode()
    offset = rcvdData
    try_move(offset)
    window['offset_label'].update(offset)
    if(event == sg.WIN_CLOSED or rcvdData == "Bye" or rcvdData == "bye"):
        break
    if event == "Start":
        started = not started
        if (started == False):
            ser.write(bytes(HOLD))
c.close()
window.close()
ser.write(bytes(HOLD))
sleep(0.5)
ser.close()