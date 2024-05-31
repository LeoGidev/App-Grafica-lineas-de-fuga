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