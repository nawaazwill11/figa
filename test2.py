from tkinter import Tk, Label
from PIL import Image, ImageTk

root = Tk()

file = './image.jpg'

image = Image.open(file)

zoom = 1.8

#multiple image size by zoom
pixels_x, pixels_y = (600, 500)

img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y))) 
label = Label(root, image=img)
label.image = img
label.pack()

root.mainloop()