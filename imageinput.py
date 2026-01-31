from tkinter import*
from PIL import ImageTk,Image
root=Tk()
img=PhotoImage(file="rashi creative .png")
l=Label(root,image=img)
#l.image=img
l.place(x=0,y=0)
root.mainloop()
