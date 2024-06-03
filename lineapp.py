import tkinter as tk
from tkinter import Canvas, Frame, Button, Scale, HORIZONTAL, Label, colorchooser, ttk
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
        control_panel = Frame(main_frame, width=600)
        control_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        
        # Crear escalas para controlar la densidad de líneas
        self.horizontal_scale = Scale(control_panel, from_=1, to=0.1, resolution=0.1, orient=HORIZONTAL, label="Líneas Paredes")
        self.horizontal_scale.set(0.5)
        self.horizontal_scale.pack(pady=10)
        
        self.vertical_scale = Scale(control_panel, from_=1, to=0.1, resolution=0.1, orient=HORIZONTAL, label="Líneas Techo/Piso")
        self.vertical_scale.set(0.5)
        self.vertical_scale.pack(pady=10)
        
        # Crear escalas para controlar el grosor de las líneas
        self.line_thickness_scale = Scale(control_panel, from_=0.1, to=3, resolution=0.1, orient=HORIZONTAL, label="Grosor de Línea")
        self.line_thickness_scale.set(0.1)
        self.line_thickness_scale.pack(pady=10)
        
        # Crear escalas para controlar la transparencia de las líneas
        self.line_alpha_scale = Scale(control_panel, from_=0.1, to=1.0, resolution=0.1, orient=HORIZONTAL, label="Transparencia de Línea")
        self.line_alpha_scale.set(1)
        self.line_alpha_scale.pack(pady=10)
        
        # Selector de color
        self.color_var = tk.StringVar(value="red")
        self.color_options = ["blue", "red", "green", "pink", "black"]
        Label(control_panel, text="Color de Línea").pack(pady=10)
        self.color_menu = ttk.Combobox(control_panel, textvariable=self.color_var, values=self.color_options)
        self.color_menu.pack(pady=10)
        
        # Botón para cambiar el color de fondo
        bg_button = Button(control_panel, text="Cambiar Fondo", command=self.cambiar_fondo)
        bg_button.pack(pady=10)
        
        # Botón para limpiar el lienzo
        clear_button = Button(control_panel, text="Limpiar Lienzo", command=self.limpiar_lienzo)
        clear_button.pack(pady=10)
        
        # Botón para guardar la imagen
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
            line_thickness = self.line_thickness_scale.get()
            line_alpha = self.line_alpha_scale.get()
            color = self.color_var.get()
            
            # Dibujar punto de fuga
            self.canvas.create_oval(x_fuga, y_fuga, x_fuga+1, y_fuga+1, fill="green")
            
            # Dibujar líneas de fuga horizontales
            for y in range(0, self.height_px+1, int(self.dpi * horizontal_spacing)):
                self.canvas.create_line(0, y, x_fuga, y_fuga, fill="black", width=line_thickness)
                self.canvas.create_line(self.width_px, y, x_fuga, y_fuga, fill="black", width=line_thickness)
            
            # Dibujar líneas de fuga verticales
            for x in range(0, self.width_px+1, int(self.dpi * vertical_spacing)):
                self.canvas.create_line(x, 0, x_fuga, y_fuga, fill="red", width=line_thickness)
                self.canvas.create_line(x, self.height_px, x_fuga, y_fuga, fill="red", width=line_thickness)
            
            # Dibujar líneas verdes horizontales debajo del punto de fuga dentro del triángulo
            for y in range(y_fuga, self.height_px+1, int(self.dpi * horizontal_spacing)):
                left_intercept_x = x_fuga - (x_fuga * (y - y_fuga) / y_fuga)
                right_intercept_x = x_fuga + ((self.width_px - x_fuga) * (y - y_fuga) / y_fuga)
                if left_intercept_x >= 0 and right_intercept_x <= self.width_px:
                    self.canvas.create_line(left_intercept_x, y, right_intercept_x, y, fill="green", width=line_thickness)
            
            # Dibujar líneas rosadas horizontales encima del punto de fuga dentro del triángulo
            for y in range(0, y_fuga, int(self.dpi * horizontal_spacing)):
                left_intercept_x = x_fuga - (x_fuga * (y_fuga - y) / y_fuga)
                right_intercept_x = x_fuga + ((self.width_px - x_fuga) * (y_fuga - y) / y_fuga)
                if left_intercept_x >= 0 and right_intercept_x <= self.width_px:
                    self.canvas.create_line(left_intercept_x, y, right_intercept_x, y, fill="yellow", width=line_thickness)

    def cambiar_fondo(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.canvas.config(bg=color)

    def limpiar_lienzo(self):
        self.canvas.delete("all")
        self.punto_fuga = None

    def guardar_imagen(self):
        if self.punto_fuga is None:
            return
        
        # Obtener los valores de espaciado de las escalas
        horizontal_spacing = self.horizontal_scale.get()
        vertical_spacing = self.vertical_scale.get()
        line_thickness = self.line_thickness_scale.get()
        line_alpha = self.line_alpha_scale.get()
        color = self.color_var.get()
        
        fig, ax = plt.subplots(figsize=(self.width_px / self.dpi, self.height_px / self.dpi), dpi=self.dpi)
        ax.set_xlim(0, self.width_px)
        ax.set_ylim(0, self.height_px)
        ax.invert_yaxis()
        ax.set_axis_off()

        x_fuga, y_fuga = self.punto_fuga
        
        # Dibujar líneas de fuga horizontales
        for y in range(0, self.height_px+1, int(self.dpi * horizontal_spacing)):
            ax.plot([0, x_fuga], [y, y_fuga], color=color, linewidth=line_thickness, alpha=line_alpha)
            ax.plot([self.width_px, x_fuga], [y, y_fuga], color=color, linewidth=line_thickness, alpha=line_alpha)
        
        # Dibujar líneas de fuga verticales
        for x in range(0, self.width_px+1, int(self.dpi * vertical_spacing)):
            ax.plot([x, x_fuga], [0, y_fuga], color=color, linewidth=line_thickness, alpha=line_alpha)
            ax.plot([x, x_fuga], [self.height_px, y_fuga], color=color, linewidth=line_thickness, alpha=line_alpha)
        
        # Dibujar líneas verdes horizontales debajo del punto de fuga dentro del triángulo
        for y in range(y_fuga, self.height_px+1, int(self.dpi * horizontal_spacing)):
            left_intercept_x = x_fuga - (x_fuga * (y - y_fuga) / y_fuga)
            right_intercept_x = x_fuga + ((self.width_px - x_fuga) * (y - y_fuga) / y_fuga)
            if left_intercept_x >= 0 and right_intercept_x <= self.width_px:
                ax.plot([left_intercept_x, right_intercept_x], [y, y], color="green", linewidth=line_thickness, alpha=line_alpha)
        
        # Dibujar líneas rosadas horizontales encima del punto de fuga dentro del triángulo
        for y in range(0, y_fuga, int(self.dpi * horizontal_spacing)):
            left_intercept_x = x_fuga - (x_fuga * (y_fuga - y) / y_fuga)
            right_intercept_x = x_fuga + ((self.width_px - x_fuga) * (y_fuga - y) / y_fuga)
            if left_intercept_x >= 0 and right_intercept_x <= self.width_px:
                ax.plot([left_intercept_x, right_intercept_x], [y, y], color="pink", linewidth=line_thickness, alpha=line_alpha)
        
        # Dibujar punto de fuga
        ax.plot(x_fuga, y_fuga, 'ro', markersize=1)

        plt.axis('off')
        plt.gca().set_facecolor((0,0,0,0))  # Hacer el fondo transparente
        plt.savefig('lineas_de_fuga.png', bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = LineasDeFugaApp(root, width_cm=4, height_cm=3, dpi=200)
    root.mainloop()







