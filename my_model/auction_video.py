# Source - https://stackoverflow.com/a/76674577
# Posted by Prem Sinha, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-01, License - CC BY-SA 4.0

import cv2 as cv
import numpy as np
from time import time
from mss import mss
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
import Quartz

windowName = "Google Chrome"  


def get_window_dimensions(hwnd):
    window_info_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionIncludingWindow, hwnd)

    for window_info in window_info_list:
        window_id = window_info[Quartz.kCGWindowNumber]
        if window_id == hwnd:
            bounds = window_info[Quartz.kCGWindowBounds]
            width = bounds['Width']
            height = bounds['Height']
            left = bounds['X']
            top = bounds['Y']
            return {"top": top, "left": left, "width": width, "height": height}

    return None


def window_capture():
    loop_time = time()
    windowList = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)

    for window in windowList:
        print(window.get('kCGWindowName', ''))
        if windowName.lower() in window.get('kCGWindowName', '').lower():
            hwnd = window['kCGWindowNumber']
            print('found window id %s' % hwnd)

    monitor = get_window_dimensions(hwnd)

    with mss() as sct:
        # monitor = {"top": 40, "left": 0, "width": 800, "height": 600}

        while (True):

            screenshot = np.array(sct.grab(monitor))
            screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

            cv.imshow('Computer Vision', screenshot)

            print('FPS {}'.format(1 / (time() - loop_time)))
            loop_time = time()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break


window_capture()

print('Done.')
