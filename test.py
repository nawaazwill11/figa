from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()

loadingAreaTxt = tk.Text(root, wrap="char", borderwidth=0, highlightthickness=0, state="disabled", cursor='arrow', relief='flat', bg='pink')
loadingAreaTxt.pack(fill="both", expand=1)

element = tk.Frame(loadingAreaTxt, bd=1, relief="sunken", background='green', width=100, height=100)
image = Image.open('./image.jpg')
tkimage = ImageTk.PhotoImage(image)
image_container= tk.Label(element, image=tkimage)
image_container.pack()
loadingAreaTxt.window_create(tk.END, window=element, padx=10, pady=10)
root.mainloop()