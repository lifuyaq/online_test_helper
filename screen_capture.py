import tkinter as tk
from PIL import ImageGrab
import PIL
from datetime import datetime
import os
import time
import re
import text_recognition

import sys

from draw_rectangle import mapping_coordinate


def suppose_scourier(image: PIL.Image.Image):
    return text_recognition.main_func(image)


def test():
    return {
        "question": "This is a question",
        "answer": "This is a answer"
    }


class TransparentScreenCapture:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture")

        # Make window frameless
        # self.root.overrideredirect(True)

        # Set window transparency (0.3 = 70% transparent)
        self.root.attributes('-alpha', 0.3)

        # Always on top
        self.root.attributes('-topmost', True)

        # Default size
        self.width = 400
        self.height = 200

        # Create main frame with black background
        self.main_frame = tk.Frame(
            self.root,
            bg='black',
            highlightthickness=2,
            highlightbackground='black'
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events for dragging
        self.main_frame.bind('<Button-1>', self.start_move)
        self.main_frame.bind('<B1-Motion>', self.on_move)
        self.main_frame.bind('<Enter>', self.on_enter)
        self.main_frame.bind('<Leave>', self.on_leave)

        # Create button frame
        button_frame = tk.Frame(self.main_frame, bg='black')
        button_frame.pack(side=tk.BOTTOM, pady=5)

        # Create capture button
        self.capture_btn = tk.Button(
            button_frame,
            text="Search",
            command=self.capture_screen,
            bg='black',
            fg='white',
            relief=tk.FLAT,
            padx=10
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)

        # Create close button
        self.close_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_answer,
            bg='black',
            fg='white',
            relief=tk.FLAT,
            padx=10
        )
        self.close_btn.pack(side=tk.LEFT, padx=5)

        # Variables for window movement
        self.x = 0
        self.y = 0

        # Create screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')

        self.current_content = None
        self.question = tk.Label(self.main_frame, text="", font=("Arial", 14),
                         fg='black',
                         bg=self.main_frame['bg']
                         )
        self.question.place(relx=0.1, rely=0.1, anchor="nw")
        self.answer = tk.Label(self.main_frame, text="", font=("Arial", 14),
                         fg='white',
                         bg=self.main_frame['bg']
                         )
        self.answer.place(relx=0.1, rely=0.4, anchor="nw")


    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        self.root.attributes('-alpha', 0.3)
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def on_enter(self, event):
        # Make window more opaque when mouse enters
        if self.current_content is None:
            self.root.attributes('-alpha', 0.5)
            self.question.config(text="")
            self.answer.config(text="")
        else:
            self.root.attributes('-alpha', 0.9)
            self.question.config(text=self.current_content["question"])
            self.answer.config(text=self.current_content["answer"])

    def on_leave(self, event):
        if self.current_content is None:
            self.root.attributes('-alpha', 0.3)
            self.question.config(text="")
            self.answer.config(text="")
        else:
            self.root.attributes('-alpha', 0.9)
            self.question.config(text=self.current_content["question"])
            self.answer.config(text=self.current_content["answer"])


    def clear_answer(self):
        self.current_content = None
        self.root.attributes('-alpha', 0.3)
        self.question.config(text="")
        self.answer.config(text="")

    def capture_screen(self):

        def get_win_position():
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            return x, y, w, h

        rect = get_win_position()
        rect = mapping_coordinate(rect)


        # Hide window temporarily for clean capture
        self.root.withdraw()
        self.root.update()

        time.sleep(1)

        x = 0
        y = 0

        # Capture the screen area
        screenshot = ImageGrab.grab(bbox=rect)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/capture_{timestamp}.png"

        # Save the screenshot
        screenshot.save(filename)

        # self.current_content = suppose_scourier(filename)
        self.current_content = test()

        self.question.config(text=self.current_content["question"])
        self.answer.config(text=self.current_content["answer"])

        # Show window again
        self.root.deiconify()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TransparentScreenCapture()
    app.run()