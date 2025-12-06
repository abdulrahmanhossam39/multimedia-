import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class ImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display GUI")
        self.root.geometry("900x600")
        
# Variables to store images
        self.gray_image = None
        self.color_image = None
        self.gray_photo = None
        self.color_photo = None
        
# Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
# Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
# Buttons
        ttk.Button(button_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Sample", command=self.generate_sample).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Images", command=self.clear_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=5)
        
# Image display frames
        self.gray_frame = ttk.LabelFrame(main_frame, text="Grayscale Image", padding="10")
        self.gray_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.color_frame = ttk.LabelFrame(main_frame, text="Color Image", padding="10")
        self.color_frame.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
# Labels to display images
        self.gray_label = ttk.Label(self.gray_frame, text="No image loaded", anchor=tk.CENTER)
        self.gray_label.pack(expand=True, fill=tk.BOTH)
        
        self.color_label = ttk.Label(self.color_frame, text="No image loaded", anchor=tk.CENTER)
        self.color_label.pack(expand=True, fill=tk.BOTH)
        
# Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
# Generate sample images on startup
        self.generate_sample()
    
    def load_image(self):
        """Load an image from file"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
# Load original color image
                img = Image.open(file_path)
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                
# Create grayscale version
                gray_img = img.convert('L')
                
# Display images
                self.display_images(gray_img, img)
                messagebox.showinfo("Success", "Image loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def generate_sample(self):
        """Generate sample gradient images"""
        width, height = 400, 300
        
# Create color gradient image
        color_img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(color_img)
        
        for y in range(height):
            for x in range(width):
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = int(((x + y) / (width + height)) * 255)
                draw.point((x, y), fill=(r, g, b))
        
# Create grayscale version
        gray_img = color_img.convert('L')
        
# Display images
        self.display_images(gray_img, color_img)
    
    def display_images(self, gray_img, color_img):
        """Display both grayscale and color images"""
# Convert to PhotoImage for tkinter
        self.gray_photo = ImageTk.PhotoImage(gray_img)
        self.color_photo = ImageTk.PhotoImage(color_img)
        
# Update labels
        self.gray_label.configure(image=self.gray_photo, text="")
        self.color_label.configure(image=self.color_photo, text="")
        
# Keep references
        self.gray_image = gray_img
        self.color_image = color_img
    
    def clear_images(self):
        """Clear both images"""
        self.gray_label.configure(image="", text="No image loaded")
        self.color_label.configure(image="", text="No image loaded")
        self.gray_image = None
        self.color_image = None
        self.gray_photo = None
        self.color_photo = None

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGUI(root)
    root.mainloop()