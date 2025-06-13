import tkinter as tk
from tkinter import Button, filedialog, Scrollbar, Canvas, Scale
from PIL import Image, ImageTk
import numpy as np

class ImageEditor:
    def __init__(self,root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry('1280x720')

        painel_frame = tk.Frame(root)
        painel_frame.pack(fill='both', expand=True)

        self.canvas = Canvas(painel_frame, bg='white')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.scroll_y = Scrollbar(painel_frame, orient='vertical', command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky='ns')

        self.scroll_x = Scrollbar(painel_frame,orient='horizontal', command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.internal_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.internal_frame, anchor='nw')

        self.internal_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        painel_frame.rowconfigure(0, weight=1)
        painel_frame.columnconfigure(0, weight=1)

        btn_frame = tk.Frame(root)
        btn_frame.pack(side='bottom', fill='x')

        self.zoom_scale = Scale(
            btn_frame,
            from_=-5, to=5,
            orient='horizontal',
            label='Zoom',
            length=200,
            showvalue=True,
            command=self._on_zoom_change
        )
        

        self.image = None
        self.original_image = None

        button_texts = [
            ("Select Image", self.select_image),
            ("Black and White", self.black_and_white),
            ("Sepsis Effect", self.sepsis_effect),
            ("Negative Effect", self.negative_effect),
            ("Sharpening Effect", self.shaperning_effect),
            ("Blur Effect", self.blur_effect),
            ("Apply Edges", self.apply_edges),
            ("Save Image", self.save_image)
        ]

        self.zoom_scale.set(0)  # Começa no centro (sem zoom)
        self.zoom_scale.grid(row=1, column=0, columnspan=len(button_texts), sticky='ew', padx=10, pady=5)
        
        for i, (text, cmd) in enumerate(button_texts):
            btn = Button(btn_frame, text=text, command=cmd)
            btn.grid(row=0, column=i, sticky='nsew', padx=5, pady=10)
            btn_frame.columnconfigure(i, weight=1)

    def select_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files","*.jpg *.jpeg *.png")])
        if file:
            self.image = Image.open(file)
            self.original_image = self.image.copy()
            self.original_image_backup = self.image.copy()
            self.display_image(self.image)

    def display_image(self, img):
        self.image_display = ImageTk.PhotoImage(img)
        for widget in self.internal_frame.winfo_children():
            widget.destroy()
        label = tk.Label(self.internal_frame, image=self.image_display)
        label.pack()

    def black_and_white(self):
        if self.original_image:
            width, height = self.original_image.size
            image_bw = Image.new("RGB", (width,height))
            original_pixels = self.original_image.load()
            bw_pixels = image_bw.load()

            for x in range(width):
                for y in range(height):
                    r, g, b = original_pixels[x, y][:3]
                    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                    bw_pixels[x, y] = (gray, gray, gray)
            
            self.image = image_bw
            self.display_image(self.image)

    def sepsis_effect(self):
        if self.original_image:
            width, height = self.original_image.size
            sepsis_image = self.original_image.copy()
            pixels = sepsis_image.load()

            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y][:3]

                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    tr = min(255, tr)
                    tg = min(255, tg)
                    tb = min(255, tb)

                    pixels[x, y] = (tr, tg, tb)
            
            self.image = sepsis_image
            self.display_image(self.image)

    def negative_effect(self):
        if self.original_image:
            width, height = self.original_image.size
            negative_image = self.original_image.copy()
            pixels = negative_image.load()

            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y][:3]

                    r_neg = 255 - r
                    g_neg = 255 - g
                    b_neg = 255 - b

                    pixels[x, y] = (r_neg, g_neg, b_neg)
            
            self.image = negative_image
            self.display_image(self.image)
    
    def apply_rgb_filter(self, kernel):
        if self.original_image_backup:
            image_rgb = self.original_image_backup.convert("RGB")
            matrix = np.array(image_rgb, dtype=np.float32)
            height, width, channels = matrix.shape
            output = np.zeros_like(matrix)

            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    for c in range(3):
                        region = matrix[y - 1:y + 2, x - 1:x + 2, c]
                        value = np.sum(region * kernel)
                        output[y, x, c] = np.clip(value, 0, 255)

            return Image.fromarray(output.astype(np.uint8))

    def shaperning_effect(self):
        kernel = np.array(
                [[0, -1, 0],
                [-1, 5 , -1],
                [0, -1, 0]
                ])
        img = self.apply_rgb_filter(kernel)
        if img:
            self.image = img
            self.original_image = img
            self.display_image(img)

    def blur_effect(self):
        kernel = np.ones((3, 3)) / 9
        img = self.apply_rgb_filter(kernel)
        if img:
            self.image = img
            self.original_image = img
            self.display_image(img)

    def apply_edges(self):
        kernel = np.array(
                [[0, -1, 0],
                 [-1, 4, -1],
                 [0, -1, 0]
        ])
        img = self.apply_rgb_filter(kernel)
        if img:
            self.image = img
            self.original_image = img
            self.display_image(img)
    
    def save_image(self):
        if self.image:
            path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG","*.png"),
                                                           ("JPEG","*.jpg"), 
                                                           ("All Files","*.*")])
            if path:
                self.image.save(path)

    def _on_zoom_change(self, value):
        if self.original_image:
            zoom_factor = 1.0 + (int(value) / 10.0)
            if zoom_factor <= 0:
                zoom_factor = 0.1
            width, height = self.original_image.size
            new_size = (int(width * zoom_factor), int(height * zoom_factor))
            zoomed_img = self.original_image.resize(new_size, Image.LANCZOS)
            self.image = zoomed_img
            self.display_image(self.image)


root = tk.Tk()
app = ImageEditor(root)
root.mainloop()