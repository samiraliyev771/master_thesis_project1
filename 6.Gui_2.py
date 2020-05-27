import tkinter

window = tkinter.Tk()
window.geometry("360x280")
# Code to add widgets will go here...

# to rename the title of the window
window.title("Sign Language Recognizer")

# pack is used to show the object in the window
label = tkinter.Label(window, text = "To start the scan, press the below button!",
                      font=('Times New Roman', 12, 'bold'))
label.pack()

# button widget
button_scan = tkinter.Button(window,text="Start Gesture Scan", fg='blue', bg='white',
                             font=('Times New Roman', 10, 'bold'), bd=5)
button_scan.place(x=120, y=100)
#button_scan.pack()


window.lift()

window.mainloop()
