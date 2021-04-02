import ctypes
import os 
import struct
import win32gui
import win32con
import win32api
import time
import tkinter

from threading import Timer, Thread, Event
from PIL import Image, ImageTk


image_name = 'test.jpg'
image_path = os.path.abspath(image_name)#,image)
SPI_SETDESKWALLPAPER = 20




def is_64bit_windows():
    return struct.calcsize('P')*8 == 64

if is_64bit_windows():
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
else:
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 3)

windows = []
#print(win32gui.FindWindow(None, ''))

def isRealWindows(hWnd):
    myhWnd = win32api.FindWindow(None, 'app')

    if myhWnd == hWnd():
        return False 
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True

    return False
    

def test(hWnd, windows):
    if not isRealWindows(hWnd):
        return
    windows.append(hWnd)
    win32gui.SetWindowLong(hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
    win32gui.SetLayeredWindowAttributes(hWnd, win32api.RGB(0,0,0), 0, win32con.LWA_ALPHA)


def HiddenAllWindows():
    win32gui.EnumWindows(test, windows)

class perpetualTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

def CreateMyWindow():
    root = tkinter.Tk() 
    root.title("app")
    root.attributes('-fullscreen', True)
    root.lift()

    frame = tkinter.Frame(root)
    frame.grid()



    canvas = tkinter.Canvas(root, height=1080, width=1920)
    path_image = os.path.abspath('test.jpg')
    image = Image.open(path_image)
    photo = ImageTk.PhotoImage(image)
    image = canvas.create_image(0, 0, anchor='nw',image=photo)
    canvas.grid(row = 1, column=1)

    tkinter.mainloop()

CreateMyWindow()
MyTest = perpetualTimer(0.5, HiddenAllWindows)
MyTest.start()


time.sleep(10)

MyTest.cancel()

#os.system('C:\\Windows\\explorer.exe')

for hWnd in windows:
    win32gui.SetWindowLong(hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
    win32gui.SetLayeredWindowAttributes(hWnd, win32api.RGB(0,0,0), 255, win32con.LWA_ALPHA)

