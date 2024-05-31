import tkinter as tk
from tkinter import Canvas
import matplotlib.pyplot as plt

class LineasDeFugaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Líneas de Fuga para Bocetos de Ciudades")
        
        self.canvas = Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.obtener_punto_fuga)
        
        self.punto_fuga = None

    def obtener_punto_fuga(self, event):
            self.punto_fuga = (event.x, event.y)
            self.dibujar_lineas_de_fuga()

    def dibujar_lineas_de_fuga(self):
        if self.punto_fuga:
            self.canvas.delete("all")
            x_fuga, y_fuga = self.punto_fuga
            
            # Dibujar punto de fuga
            self.canvas.create_oval(x_fuga-5, y_fuga-5, x_fuga+5, y_fuga+5, fill="red")
            
            # Dibujar líneas de fuga horizontales
            for y in range(0, 601, 50):
                self.canvas.create_line(0, y, x_fuga, y_fuga, fill="blue")
                self.canvas.create_line(800, y, x_fuga, y_fuga, fill="blue")
            
            # Dibujar líneas de fuga verticales
            for x in range(0, 801, 50):
                self.canvas.create_line(x, 0, x_fuga, y_fuga, fill="blue")
                self.canvas.create_line(x, 600, x_fuga, y_fuga, fill="blue")