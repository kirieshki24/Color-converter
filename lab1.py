import customtkinter as ctk
from tkinter import messagebox
import colorsys
from skimage import color
import PIL
from CTkColorPicker import *
import numpy as np

# Functions for color conversion
def rgb_to_cmyk(r, g, b_rgb):
    if (r == 0) and (g == 0) and (b_rgb == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b_rgb / 255
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c / 100) * (1 - k / 100)
    g = 255 * (1 - m / 100) * (1 - k / 100)
    b_rgb = 255 * (1 - y / 100) * (1 - k / 100)
    return round(r), round(g), round(b_rgb)

def rgb_to_lab(r, g, b_rgb):
    rgb_norm = np.array([r, g, b_rgb]) / 255.0
    lab = color.rgb2lab(rgb_norm.reshape(1, 1, 3))
    return tuple(lab.flatten())

def lab_to_rgb(l, a, b_lab):
    lab = np.array([l, a, b_lab])
    rgb = color.lab2rgb(lab.reshape(1, 1, 3)) * 255
    return tuple(np.clip(rgb.flatten(), 0, 255).astype(int))

# GUI Application
class ColorConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Color Converter")
        self.configure(background="red")

        # RGB Sliders and Entries
        self.rgb_label = ctk.CTkLabel(self, text="RGB")
        self.rgb_label.grid(row=0, column=0, padx=10, pady=10)

        self.r_slider = ctk.CTkSlider(self, from_=0, to=255, number_of_steps=255, command=self.update_from_rgb)
        self.r_slider.grid(row=0, column=1, padx=10, pady=10)
        self.r_entry = ctk.CTkEntry(self, placeholder_text="R", width=50)
        self.r_entry.grid(row=0, column=2, padx=10, pady=10)
        self.r_entry.bind("<Return>", self.update_rgb_from_entry)

        self.g_slider = ctk.CTkSlider(self, from_=0, to=255, number_of_steps=255, command=self.update_from_rgb)
        self.g_slider.grid(row=0, column=3, padx=10, pady=10)
        self.g_entry = ctk.CTkEntry(self, placeholder_text="G", width=50)
        self.g_entry.grid(row=0, column=4, padx=10, pady=10)
        self.g_entry.bind("<Return>", self.update_rgb_from_entry)

        self.b_slider = ctk.CTkSlider(self, from_=0, to=255, number_of_steps=255, command=self.update_from_rgb)
        self.b_slider.grid(row=0, column=5, padx=10, pady=10)
        self.b_entry = ctk.CTkEntry(self, placeholder_text="B", width=50)
        self.b_entry.grid(row=0, column=6, padx=10, pady=10)
        self.b_entry.bind("<Return>", self.update_rgb_from_entry)

        # CMYK Sliders and Entries
        self.cmyk_label = ctk.CTkLabel(self, text="CMYK")
        self.cmyk_label.grid(row=1, column=0, padx=10, pady=10)

        self.c_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.update_from_cmyk)
        self.c_slider.grid(row=1, column=1, padx=10, pady=10)
        self.c_entry = ctk.CTkEntry(self, placeholder_text="C", width=50)
        self.c_entry.grid(row=1, column=2, padx=10, pady=10)
        self.c_entry.bind("<Return>", self.update_cmyk_from_entry)

        self.m_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.update_from_cmyk)
        self.m_slider.grid(row=1, column=3, padx=10, pady=10)
        self.m_entry = ctk.CTkEntry(self, placeholder_text="M", width=50)
        self.m_entry.grid(row=1, column=4, padx=10, pady=10)
        self.m_entry.bind("<Return>", self.update_cmyk_from_entry)

        self.y_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.update_from_cmyk)
        self.y_slider.grid(row=1, column=5, padx=10, pady=10)
        self.y_entry = ctk.CTkEntry(self, placeholder_text="Y", width=50)
        self.y_entry.grid(row=1, column=6, padx=10, pady=10)
        self.y_entry.bind("<Return>", self.update_cmyk_from_entry)

        self.k_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.update_from_cmyk)
        self.k_slider.grid(row=1, column=7, padx=10, pady=10)
        self.k_entry = ctk.CTkEntry(self, placeholder_text="K", width=50)
        self.k_entry.grid(row=1, column=8, padx=10, pady=10)
        self.k_entry.bind("<Return>", self.update_cmyk_from_entry)

        # LAB Sliders and Entries
        self.lab_label = ctk.CTkLabel(self, text="LAB")
        self.lab_label.grid(row=2, column=0, padx=10, pady=10)

        self.l_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.update_from_lab)
        self.l_slider.grid(row=2, column=1, padx=10, pady=10)
        self.l_entry = ctk.CTkEntry(self, placeholder_text="L", width=50)
        self.l_entry.grid(row=2, column=2, padx=10, pady=10)
        self.l_entry.bind("<Return>", self.update_lab_from_entry)

        self.a_slider = ctk.CTkSlider(self, from_=-128, to=128, number_of_steps=256, command=self.update_from_lab)
        self.a_slider.grid(row=2, column=3, padx=10, pady=10)
        self.a_entry = ctk.CTkEntry(self, placeholder_text="A", width=50)
        self.a_entry.grid(row=2, column=4, padx=10, pady=10)
        self.a_entry.bind("<Return>", self.update_lab_from_entry)

        self.b_lab_slider = ctk.CTkSlider(self, from_=-128, to=128, number_of_steps=256, command=self.update_from_lab)
        self.b_lab_slider.grid(row=2, column=5, padx=10, pady=10)
        self.b_lab_entry = ctk.CTkEntry(self, placeholder_text="B", width=50)
        self.b_lab_entry.grid(row=2, column=6, padx=10, pady=10)
        self.b_lab_entry.bind("<Return>", self.update_lab_from_entry)

        # Button to choose color from palette
        self.color_palette_button = ctk.CTkButton(self, text="Choose Color", command=self.choose_color, fg_color="black")
        self.color_palette_button.grid(row=3, column=0, columnspan=9, padx=10, pady=10)

    def update_from_rgb(self, value=None):
        try:
            r = int(self.r_slider.get())
            g = int(self.g_slider.get())
            b_rgb = int(self.b_slider.get())
            c, m, y, k = rgb_to_cmyk(r, g, b_rgb)
            l, a, b_lab = rgb_to_lab(r, g, b_rgb)
            self.r_entry.delete(0, ctk.END)
            self.r_entry.insert(0, str(r))
            self.g_entry.delete(0, ctk.END)
            self.g_entry.insert(0, str(g))
            self.b_entry.delete(0, ctk.END)
            self.b_entry.insert(0, str(b_rgb))

            # Update CMYK
            self.c_slider.set(c)
            self.m_slider.set(m)
            self.y_slider.set(y)
            self.k_slider.set(k)
            self.c_entry.delete(0, ctk.END)
            self.c_entry.insert(0, str(c))
            self.m_entry.delete(0, ctk.END)
            self.m_entry.insert(0, str(m))
            self.y_entry.delete(0, ctk.END)
            self.y_entry.insert(0, str(y))
            self.k_entry.delete(0, ctk.END)
            self.k_entry.insert(0, str(k))

            # Update LAB
            self.l_slider.set(l)
            self.a_slider.set(a)
            self.b_lab_slider.set(b_lab)
            self.l_entry.delete(0, ctk.END)
            self.l_entry.insert(0, str(l))
            self.a_entry.delete(0, ctk.END)
            self.a_entry.insert(0, str(a))
            self.b_lab_entry.delete(0, ctk.END)
            self.b_lab_entry.insert(0, str(b_lab))
        except ValueError:
            messagebox.showwarning("Input Error", "RGB values must be between 0 and 255")

    def update_rgb_from_entry(self, event=None):
        try:
            r = int(self.r_entry.get())
            g = int(self.g_entry.get())
            b_rgb = int(self.b_entry.get())
            self.r_slider.set(r)
            self.g_slider.set(g)
            self.b_slider.set(b_rgb)
            self.update_from_rgb()
        except ValueError:
            messagebox.showwarning("Input Error", "RGB values must be between 0 and 255")

    def update_from_cmyk(self, value=None):
        try:
            c = int(self.c_slider.get())
            m = int(self.m_slider.get())
            y = int(self.y_slider.get())
            k = int(self.k_slider.get())
            r, g, b_rgb = cmyk_to_rgb(c, m, y, k)
            l, a, b_lab = rgb_to_lab(r, g, b_rgb)
            self.c_entry.delete(0, ctk.END)
            self.c_entry.insert(0, str(c))
            self.m_entry.delete(0, ctk.END)
            self.m_entry.insert(0, str(m))
            self.y_entry.delete(0, ctk.END)
            self.y_entry.insert(0, str(y))
            self.k_entry.delete(0, ctk.END)
            self.k_entry.insert(0, str(k))

            # Update RGB
            self.r_slider.set(r)
            self.g_slider.set(g)
            self.b_slider.set(b_rgb)
            self.r_entry.delete(0, ctk.END)
            self.r_entry.insert(0, str(r))
            self.g_entry.delete(0, ctk.END)
            self.g_entry.insert(0, str(g))
            self.b_entry.delete(0, ctk.END)
            self.b_entry.insert(0, str(b_rgb))

            # Update LAB
            self.l_slider.set(l)
            self.a_slider.set(a)
            self.b_lab_slider.set(b_lab)
            self.l_entry.delete(0, ctk.END)
            self.l_entry.insert(0, str(l))
            self.a_entry.delete(0, ctk.END)
            self.a_entry.insert(0, str(a))
            self.b_lab_entry.delete(0, ctk.END)
            self.b_lab_entry.insert(0, str(b_lab))
        except ValueError:
            messagebox.showwarning("Input Error", "CMYK values must be between 0 and 100")

    def update_cmyk_from_entry(self, event=None):
        try:
            c = int(self.c_entry.get())
            m = int(self.m_entry.get())
            y = int(self.y_entry.get())
            k = int(self.k_entry.get())
            self.c_slider.set(c)
            self.m_slider.set(m)
            self.y_slider.set(y)
            self.k_slider.set(k)
            self.update_from_cmyk()
        except ValueError:
            messagebox.showwarning("Input Error", "CMYK values must be between 0 and 100")

    def update_from_lab(self, value=None):
        try:
            l = float(self.l_slider.get())
            a = float(self.a_slider.get())
            b_lab = float(self.b_lab_slider.get())
            r, g, b_rgb = lab_to_rgb(l, a, b_lab)
            c, m, y, k = rgb_to_cmyk(r, g, b_rgb)
            self.l_entry.delete(0, ctk.END)
            self.l_entry.insert(0, str(l))
            self.a_entry.delete(0, ctk.END)
            self.a_entry.insert(0, str(a))
            self.b_lab_entry.delete(0, ctk.END)
            self.b_lab_entry.insert(0, str(b_lab))

            # Update RGB
            self.r_slider.set(r)
            self.g_slider.set(g)
            self.b_slider.set(b_rgb)
            self.r_entry.delete(0, ctk.END)
            self.r_entry.insert(0, str(r))
            self.g_entry.delete(0, ctk.END)
            self.g_entry.insert(0, str(g))
            self.b_entry.delete(0, ctk.END)
            self.b_entry.insert(0, str(b_rgb))

            # Update CMYK
            self.c_slider.set(c)
            self.m_slider.set(m)
            self.y_slider.set(y)
            self.k_slider.set(k)
            self.c_entry.delete(0, ctk.END)
            self.c_entry.insert(0, str(c))
            self.m_entry.delete(0, ctk.END)
            self.m_entry.insert(0, str(m))
            self.y_entry.delete(0, ctk.END)
            self.y_entry.insert(0, str(y))
            self.k_entry.delete(0, ctk.END)
            self.k_entry.insert(0, str(k))
        except ValueError:
            messagebox.showwarning("Input Error", "LAB values are out of bounds")

    def update_lab_from_entry(self, event=None):
        try:
            l = float(self.l_entry.get())
            a = float(self.a_entry.get())
            b_lab = float(self.b_lab_entry.get())
            self.l_slider.set(l)
            self.a_slider.set(a)
            self.b_lab_slider.set(b_lab)
            self.update_from_lab()
        except ValueError:
            messagebox.showwarning("Input Error", "LAB values must be within their bounds")

    def choose_color(self):
        pick_color = AskColor() # open the color picker
        color_code = pick_color.get()
        if color_code:
            r, g, b_rgb = map(int, color_code[0])
            self.r_slider.set(r)
            self.g_slider.set(g)
            self.b_slider.set(b_rgb)
            self.update_from_rgb()
# Running the app
if __name__ == "__main__":
    app = ColorConverterApp()
    app.mainloop()
