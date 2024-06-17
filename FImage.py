import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Canvas, Frame, Button
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("FotoFlex")
        self.root.geometry("1000x800")
        self.root.config(bg='white')

        self.frame = Frame(self.root, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = Canvas(self.frame, width=800, height=600, bg='white')
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.image_path = None
        self.image = None
        self.tk_image = None
        self.history = []  # To keep track of image history for undo

        # Menu
        menubar = tk.Menu(root, bg='white', fg='black', tearoff=0)
        root.config(menu=menubar)

        # Toolbar
        toolbar = Frame(self.frame, bg='white')
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bottom Buttons
        top_toolbar = Frame(self.frame, bg='white')
        top_toolbar.pack(side=tk.TOP, fill=tk.X)

        open_btn = Button(top_toolbar, text="Open", command=self.open_image, bg='white', padx=10, pady=5)
        open_btn.pack(side=tk.LEFT, padx=5, pady=5)

        save_btn = Button(top_toolbar, text="Save", command=self.save_image, bg='white', padx=10, pady=5)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        undo_btn = Button(top_toolbar, text="Undo", command=self.undo_action, bg='white', padx=10, pady=5)
        undo_btn.pack(side=tk.LEFT, padx=5, pady=5)

        exit_btn = Button(top_toolbar, text="Exit", command=root.quit, bg='white', padx=10, pady=5)
        exit_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Edit Buttons
        rotate_btn = Button(toolbar, text="Rotate 90°", command=self.rotate_image, bg='white', padx=10, pady=5)
        rotate_btn.pack(side=tk.LEFT, padx=5, pady=5)

        flip_horizontal_btn = Button(toolbar, text="Flip Horizontal", command=self.flip_horizontal, bg='white', padx=10, pady=5)
        flip_horizontal_btn.pack(side=tk.LEFT, padx=5, pady=5)

        flip_vertical_btn = Button(toolbar, text="Flip Vertical", command=self.flip_vertical, bg='white', padx=10, pady=5)
        flip_vertical_btn.pack(side=tk.LEFT, padx=5, pady=5)

        grayscale_btn = Button(toolbar, text="Grayscale", command=self.convert_to_grayscale, bg='white', padx=10, pady=5)
        grayscale_btn.pack(side=tk.LEFT, padx=5, pady=5)

        crop_btn = Button(toolbar, text="Crop", command=self.crop_image, bg='white', padx=10, pady=5)
        crop_btn.pack(side=tk.LEFT, padx=5, pady=5)

        resize_btn = Button(toolbar, text="Resize", command=self.resize_image, bg='white', padx=10, pady=5)
        resize_btn.pack(side=tk.LEFT, padx=5, pady=5)

        brightness_btn = Button(toolbar, text="Brightness", command=self.adjust_brightness, bg='white', padx=10, pady=5)
        brightness_btn.pack(side=tk.LEFT, padx=5, pady=5)

        contrast_btn = Button(toolbar, text="Contrast", command=self.adjust_contrast, bg='white', padx=10, pady=5)
        contrast_btn.pack(side=tk.LEFT, padx=5, pady=5)

        blur_btn = Button(toolbar, text="Blur", command=self.apply_blur, bg='white', padx=10, pady=5)
        blur_btn.pack(side=tk.LEFT, padx=5, pady=5)

        contour_btn = Button(toolbar, text="Contour", command=self.apply_contour, bg='white', padx=10, pady=5)
        contour_btn.pack(side=tk.LEFT, padx=5, pady=5)

        detail_btn = Button(toolbar, text="Detail", command=self.apply_detail, bg='white', padx=10, pady=5)
        detail_btn.pack(side=tk.LEFT, padx=5, pady=5)

        sharpen_btn = Button(toolbar, text="Sharpen", command=self.apply_sharpen, bg='white', padx=10, pady=5)
        sharpen_btn.pack(side=tk.LEFT, padx=5, pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.history = [self.image.copy()]  # Reset history with the original image
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.image.save(file_path)
        else:
            messagebox.showerror("Error", "No image to save")

    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def update_image(self, new_image):
        self.history.append(self.image.copy())
        self.image = new_image
        self.display_image()

    def undo_action(self):
        if len(self.history) > 1:
            self.image = self.history.pop()
            self.display_image()
        else:
            messagebox.showinfo("Undo", "No more actions to undo")

    def rotate_image(self):
        if self.image:
            new_image = self.image.rotate(90, expand=True)
            self.update_image(new_image)

    def flip_horizontal(self):
        if self.image:
            new_image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.update_image(new_image)

    def flip_vertical(self):
        if self.image:
            new_image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            self.update_image(new_image)

    def convert_to_grayscale(self):
        if self.image:
            new_image = ImageOps.grayscale(self.image)
            self.update_image(new_image)

    def crop_image(self):
        if self.image:
            left = simpledialog.askinteger("Input", "Left:")
            top = simpledialog.askinteger("Input", "Top:")
            right = simpledialog.askinteger("Input", "Right:")
            bottom = simpledialog.askinteger("Input", "Bottom:")
            if None not in (left, top, right, bottom):
                new_image = self.image.crop((left, top, right, bottom))
                self.update_image(new_image)

    def resize_image(self):
        if self.image:
            width = simpledialog.askinteger("Input", "Width:")
            height = simpledialog.askinteger("Input", "Height:")
            if None not in (width, height):
                new_image = self.image.resize((width, height), Image.ANTIALIAS)
                self.update_image(new_image)

    def adjust_brightness(self):
        if self.image:
            brightness = simpledialog.askfloat("Input", "Brightness (0.0 - 2.0):", minvalue=0.0, maxvalue=2.0)
            if brightness is not None:
                enhancer = ImageEnhance.Brightness(self.image)
                new_image = enhancer.enhance(brightness)
                self.update_image(new_image)

    def adjust_contrast(self):
        if self.image:
            contrast = simpledialog.askfloat("Input", "Contrast (0.0 - 2.0):", minvalue=0.0, maxvalue=2.0)
            if contrast is not None:
                enhancer = ImageEnhance.Contrast(self.image)
                new_image = enhancer.enhance(contrast)
                self.update_image(new_image)

    def apply_blur(self):
        if self.image:
            new_image = self.image.filter(ImageFilter.BLUR)
            self.update_image(new_image)

    def apply_contour(self):
        if self.image:
            new_image = self.image.filter(ImageFilter.CONTOUR)
            self.update_image(new_image)

    def apply_detail(self):
        if self.image:
            new_image = self.image.filter(ImageFilter.DETAIL)
            self.update_image(new_image)

    def apply_sharpen(self):
        if self.image:
            new_image = self.image.filter(ImageFilter.SHARPEN)
            self.update_image(new_image)

if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()
