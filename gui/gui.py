import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
from pathlib import Path
import os


class FromToGUI:
    def __init__(self, theme='light'):
        # Path initialization
        self.source_folder = ""
        self.destination_folder = ""

        self.theme = theme
        self._setup_paths()
        # Images path
        self.BACKGROUND_PATH = os.path.join(self.IMAGES_DIR, '6.png')
        self.LOGO_PATH = os.path.join(self.IMAGES_DIR, '5.png')
        self.BUTTON1_ANIM_PATHS = {
            'normal': [os.path.join(self.IMAGES_DIR, '1.1.png')],
            'hover': [os.path.join(self.IMAGES_DIR, '1.2.png')],
            'pressed': [os.path.join(self.IMAGES_DIR, '1.3.png')]
        }
        self.BUTTON2_ANIM_PATHS = {
            'normal': [os.path.join(self.IMAGES_DIR, '2.1.png')],
            'hover': [os.path.join(self.IMAGES_DIR, '2.2.png')],
            'pressed': [os.path.join(self.IMAGES_DIR, '2.3.png')]
        }
        self.BUTTON3_ANIM_PATHS = {
            'normal': [os.path.join(self.IMAGES_DIR, '3.1.png')],
            'hover': [os.path.join(self.IMAGES_DIR, '3.2.png')],
            'pressed': [os.path.join(self.IMAGES_DIR, '3.3.png')]
        }
        self.EXIT_BTN_IMAGES = {
            'normal': os.path.join(self.IMAGES_DIR, "7.1.png"),
            'hover': os.path.join(self.IMAGES_DIR, "7.2.png"),
            'pressed': os.path.join(self.IMAGES_DIR, "7.3.png")
        }
        self.PROGRESS_BAR_PATH = os.path.join(self.IMAGES_DIR, '4.png')

        # Size and Positions
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 720
        self.LOGO_POS = (40, 40)
        self.BUTTON1_POS = (320, 220)
        self.BUTTON2_POS = (320, 340)
        self.BUTTON3_POS = (320, 520)
        self.PROGRESS_FIELD_POS = (40, 640)

        # Event handler
        self.on_select_source = None
        self.on_select_destination = None
        self.on_move_copy = None
        self.on_exit = None

        # Gui initialization
        self._init_gui()

    def _init_gui(self):
        # Main Window Creation
        self.root = tk.Tk()
        self.root.title("FromTo")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        # Backgrounf loading
        background_img = Image.open(self.BACKGROUND_PATH).resize((640, 720))
        self.background_photo = ImageTk.PhotoImage(background_img)

        self.canvas = tk.Canvas(self.root, width=self.WINDOW_WIDTH,
                                height=self.WINDOW_HEIGHT,
                                highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.background_photo,
                                 anchor='nw')

        # Logo
        logo_img = Image.open(self.LOGO_PATH)
        self.logo_photo = ImageTk.PhotoImage(logo_img.resize((270, 81)))
        self.canvas.create_image(self.LOGO_POS[0], self.LOGO_POS[1],
                                 image=self.logo_photo, anchor='nw')

        # Window Moving
        self.canvas.bind("<ButtonPress-1>", self._start_move)
        self.canvas.bind("<B1-Motion>", self._do_move)

        # Buttons creation
        self._create_buttons()
        self._init_image_progress_bar()
        self._create_exit_button()

    def _setup_paths(self):
        """Set up path according to theme"""
        self.IMAGES_DIR = os.path.join(Path(__file__).parent.parent,
                                       'resources',
                                       self.theme)

    def _start_move(self, event):
        self.root.x = event.x
        self.root.y = event.y

    def _do_move(self, event):
        delta_x = event.x - self.root.x
        delta_y = event.y - self.root.y
        new_x = self.root.winfo_x() + delta_x
        new_y = self.root.winfo_y() + delta_y
        self.root.geometry(f"+{new_x}+{new_y}")

    def _create_buttons(self):
        # Source folder choosing button
        self.btn_source = AnimatedButton(
            self.root,
            self.BUTTON1_ANIM_PATHS,
            command=self._handle_select_source
        )
        self.canvas.create_window(self.BUTTON1_POS[0], self.BUTTON1_POS[1],
                                  window=self.btn_source)

        # Destination folder choosing button
        self.btn_dest = AnimatedButton(
            self.root,
            self.BUTTON2_ANIM_PATHS,
            command=self._handle_select_destination
        )
        self.canvas.create_window(self.BUTTON2_POS[0], self.BUTTON2_POS[1],
                                  window=self.btn_dest)

        # Replacing / copying button
        self.btn_move_copy = AnimatedButton(
            self.root,
            self.BUTTON3_ANIM_PATHS,
            command=self._handle_move_copy
        )
        self.canvas.create_window(self.BUTTON3_POS[0], self.BUTTON3_POS[1],
                                  window=self.btn_move_copy)

    def _init_image_progress_bar(self):
        """Init graphical progress bar"""
        # Load full progress bar image
        self.full_progress_img = Image.open(self.PROGRESS_BAR_PATH)
        self.progress_width, self.progress_height = self.full_progress_img.size

        self.progress_canvas = tk.Canvas(
                self.root,
                width=self.progress_width,
                height=self.progress_height,
                highlightthickness=0,
                bd=0)
        self.progress_canvas.place(x=self.PROGRESS_FIELD_POS[0],
                                   y=self.PROGRESS_FIELD_POS[1])

        # Create image for current progress bar
        empty_img = Image.new('RGBA', (1, self.progress_height))
        self.current_progress_img = ImageTk.PhotoImage(empty_img)
        self.progress_image_id = self.progress_canvas.create_image(
            0, 0,
            anchor='nw',
            image=self.current_progress_img)

    def _create_exit_button(self):
        # Exit button initialization
        self.exit_normal_img = ImageTk.PhotoImage(
            Image.open(self.EXIT_BTN_IMAGES['normal'])
            )
        self.exit_hover_img = ImageTk.PhotoImage(
            Image.open(self.EXIT_BTN_IMAGES['hover'])
            )
        self.exit_pressed_img = ImageTk.PhotoImage(
            Image.open(self.EXIT_BTN_IMAGES['pressed'])
            )

        self.exit_button = tk.Label(self.root, image=self.exit_normal_img,
                                    borderwidth=0)

        # Event handling
        self.exit_button.bind('<Enter>', lambda e: self.exit_button.config(
            image=self.exit_hover_img)
                              )
        self.exit_button.bind('<Leave>', lambda e: self.exit_button.config(
            image=self.exit_normal_img)
                              )
        self.exit_button.bind(
            '<ButtonPress-1>', lambda e: self.exit_button.config(
                image=self.exit_pressed_img
                )
                              )
        self.exit_button.bind('<ButtonRelease-1>', self._handle_exit)

        self.canvas.create_window(self.WINDOW_WIDTH - 40, 40,
                                  window=self.exit_button)

    def _handle_select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_folder = path
            if self.on_select_source:
                self.on_select_source(path)

    def _handle_select_destination(self):
        path = filedialog.askdirectory()
        if path:
            self.destination_folder = path
            if self.on_select_destination:
                self.on_select_destination(path)

    def _handle_move_copy(self):
        if self.on_move_copy:
            threading.Thread(target=self.on_move_copy).start()

    def _handle_exit(self, event):
        self.exit_button.config(image=self.exit_normal_img)
        if self.on_exit:
            self.on_exit()
        else:
            self.root.destroy()

    def update_progress(self, value, max_value=100):
        """
        Progressbar updating
        :param value: current value (0-max_value)
        :param max_value: max value
        """
        if not hasattr(self, 'full_progress_img') or not self.root.winfo_exists():
            return

        try:
            # Calculate displaying width
            progress_width = max(1, int((value / max_value) * self.progress_width))

            # Cut image
            cropped_img = self.full_progress_img.crop(
                (0, 0, progress_width, self.progress_height))

            # Create new image for Tkinter
            self.current_progress_img = ImageTk.PhotoImage(cropped_img)

            # Update image on canvas
            self.progress_canvas.itemconfig(
                self.progress_image_id,
                image=self.current_progress_img)

            # Update window
            self.root.update_idletasks()

        except Exception as e:
            print(f"Error updating progress: {e}")

    def run(self):
        """Main cycle starting"""
        self.root.mainloop()


class AnimatedButton(tk.Label):
    def __init__(self, master, anim_paths, command=None):
        super().__init__(master)
        self.anim_paths = anim_paths
        self.frames_normal = [ImageTk.PhotoImage(Image.open(p)) for p in
                              anim_paths['normal']]
        self.frames_hover = [ImageTk.PhotoImage(Image.open(p)) for p in
                             anim_paths['hover']]
        self.frames_pressed = [ImageTk.PhotoImage(Image.open(p)) for p in
                               anim_paths['pressed']]
        self.current_frames = self.frames_normal
        self.frame_index = 0
        self.command = command

        self.config(image=self.frames_normal[0], borderwidth=0,
                    highlightthickness=0)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<ButtonPress-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)

        self.animate()

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.current_frames)
        self.config(image=self.current_frames[self.frame_index])
        self.after(200, self.animate)

    def on_enter(self, event):
        self.current_frames = self.frames_hover

    def on_leave(self, event):
        self.current_frames = self.frames_normal

    def on_press(self, event):
        self.current_frames = self.frames_pressed

    def on_release(self, event):
        x, y = event.x_root, event.y_root
        widget_x = event.widget.winfo_rootx()
        widget_y = event.widget.winfo_rooty()
        width = event.widget.winfo_width()
        height = event.widget.winfo_height()

        if (widget_x <= x <= widget_x + width) and \
                (widget_y <= y <= widget_y + height):
            self.current_frames = self.frames_hover
            if callable(self.command):
                threading.Thread(target=self.command).start()


def test():
    import time

    for i in range(101):
        app.update_progress(i)
        time.sleep(0.05)


if __name__ == '__main__':
    app = FromToGUI('dark')
    threading.Thread(target=test).start()
    app.run()
