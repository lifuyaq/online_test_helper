import tkinter as tk
import sys

if sys.platform.startswith('win'):
    import win32gui
    import win32api
    import win32con
    import win32ui
    import ctypes


    def color_to_rgb(color):
        # Convert color name to RGB values
        root = tk.Tk()
        rgb = root.winfo_rgb(color)
        root.destroy()
        return rgb[0] // 256, rgb[1] // 256, rgb[2] // 256


    def draw_screen_rectangle(x1, y1, w, h, color='red', thickness=2):
        # Create a device context for the entire screen
        hdc = win32gui.GetDC(0)

        try:
            # Create a pen with the specified color and thickness
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, win32api.RGB(*color_to_rgb(color)))

            # Select the pen into the device context
            old_pen = win32gui.SelectObject(hdc, pen)

            x2 = x1 + w
            y2 = y1 + h
            # Draw the rectangle
            print(f"{x1}, {y1}")
            win32gui.Rectangle(hdc, x1, y1, x2, y2)

            # Restore the original pen and delete the created pen
            win32gui.SelectObject(hdc, old_pen)
            win32gui.DeleteObject(pen)

        finally:
            # Release the device context
            win32gui.ReleaseDC(0, hdc)


    def mapping_coordinate(rect):
        ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
        scale_x = ratio
        scale_y = ratio
        x, y, w, h = rect
        x1, y1, x2, y2 = x, y, x + w, y + h
        x1, y1, x2, y2 = int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)
        return x1, y1, x2, y2

else:
    def mapping_coordinate(rect):
        x, y, w, h = rect
        x1, y1, x2, y2 = x, y, x + w, y + h
        return x1, y1, x2, y2

if __name__ == '__main__':
    ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
    print(ratio)
