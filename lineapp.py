import tkinter as tk
from tkinter import Canvas, Frame, Button, Scale, HORIZONTAL, Label
import matplotlib.pyplot as plt
import numpy as np

class LineasDeFugaApp:
    def __init__(self, root, width_cm=10, height_cm=8, dpi=200):
        self.width_px = width_cm * dpi
        self.height_px = height_cm * dpi
        self.dpi = dpi
        self.root = root
        self.root.title("Líneas de Fuga para Bocetos de Ciudades")
        
        # Crear un marco principal
        main_frame = Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)
        
        # Crear un lienzo de dibujo
        self.canvas = Canvas(main_frame, width=self.width_px, height=self.height_px, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        # Crear un panel lateral para los controles
        control_panel = Frame(main_frame, width=200)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear escalas para controlar la densidad de líneas
        self.horizontal_scale = Scale(control_panel, from_=1, to=0.1, resolution=0.1, orient=HORIZONTAL, label="Espaciado Horizontal")
        self.horizontal_scale.set(0.5)
        self.horizontal_scale.pack(pady=10)
        
        self.vertical_scale = Scale(control_panel, from_=1, to=0.1, resolution=0.1, orient=HORIZONTAL, label="Espaciado Vertical")
        self.vertical_scale.set(0.5)
        self.vertical_scale.pack(pady=10)
        
        # Botón de ejemplo en el panel de control
        save_button = Button(control_panel, text="Guardar Imagen", command=self.guardar_imagen)
        save_button.pack(pady=10)
        
        # Vincular evento de clic en el lienzo
        self.canvas.bind("<Button-1>", self.obtener_punto_fuga)
        
        self.punto_fuga = None
    
    def obtener_punto_fuga(self, event):
        self.punto_fuga = (event.x, event.y)
        self.dibujar_lineas_de_fuga()
    
    def dibujar_lineas_de_fuga(self):
        if self.punto_fuga:
            self.canvas.delete("all")
            x_fuga, y_fuga = self.punto_fuga
            
            # Obtener los valores de espaciado de las escalas
            horizontal_spacing = self.horizontal_scale.get()
            vertical_spacing = self.vertical_scale.get()
            
            # Dibujar punto de fuga
            self.canvas.create_oval(x_fuga-5, y_fuga-5, x_fuga+5, y_fuga+5, fill="red")
            
            # Dibujar líneas de fuga horizontales
            for y in range(0, self.height_px+1, int(self.dpi * horizontal_spacing)):
                self.canvas.create_line(0, y, x_fuga, y_fuga, fill="blue")
                self.canvas.create_line(self.width_px, y, x_fuga, y_fuga, fill="blue")
            
            # Dibujar líneas de fuga verticales
            for x in range(0, self.width_px+1, int(self.dpi * vertical_spacing)):
                self.canvas.create_line(x, 0, x_fuga, y_fuga, fill="red")
                self.canvas.create_line(x, self.height_px, x_fuga, y_fuga, fill="red")
    
    def guardar_imagen(self):
        if self.punto_fuga is None:
            return
        
        # Obtener los valores de espaciado de las escalas
        horizontal_spacing = self.horizontal_scale.get()
        vertical_spacing = self.vertical_scale.get()
        
        fig, ax = plt.subplots(figsize=(self.width_px / self.dpi, self.height_px / self.dpi), dpi=self.dpi)
        ax.set_xlim(0, self.width_px)
        ax.set_ylim(0, self.height_px)
        ax.invert_yaxis()

        x_fuga, y_fuga = self.punto_fuga
        
        # Dibujar líneas de fuga horizontales
        for y in range(0, self.height_px+1, int(self.dpi * horizontal_spacing)):
            ax.plot([0, x_fuga], [y, y_fuga], color="blue")
            ax.plot([self.width_px, x_fuga], [y, y_fuga], color="blue")
        
        # Dibujar líneas de fuga verticales
        for x in range(0, self.width_px+1, int(self.dpi * vertical_spacing)):
            ax.plot([x, x_fuga], [0, y_fuga], color="blue")
            ax.plot([x, x_fuga], [self.height_px, y_fuga], color="blue")
        
        # Dibujar punto de fuga
        ax.plot(x_fuga, y_fuga, 'ro')

        plt.axis('off')
        plt.savefig('lineas_de_fuga.png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = LineasDeFugaApp(root, width_cm=4, height_cm=4, dpi=100)
    root.mainloop()


