import ctypes
import os 
import struct
import win32gui
import win32con
import win32api
import time
from threading import Timer, Thread, Event

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


#HiddenAllWindows()
MyTest = perpetualTimer(1, HiddenAllWindows)
MyTest.start()


time.sleep(10)

MyTest.cancel()

#os.system('C:\\Windows\\explorer.exe')

for hWnd in windows:
    win32gui.SetWindowLong(hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
    win32gui.SetLayeredWindowAttributes(hWnd, win32api.RGB(0,0,0), 255, win32con.LWA_ALPHA)

