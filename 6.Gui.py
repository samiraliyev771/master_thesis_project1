import tkinter
import os, signal
from subprocess import Popen
import subprocess
#import OpenCV_v1_4
import cv2

window = tkinter.Tk()
window.geometry("360x280")
# Code to add widgets will go here...

# to rename the title of the window
window.title("Sign Language Recognizer")

# labels
label1 = tkinter.Label(window, text = "To start the scan, press the below button!",
                      font=('Times New Roman', 12, 'bold'))
label1.pack()        # pack is used to show the object in the window

label2 = tkinter.Label(window, text = "To stop the scan, press the 'q'",
                      font=('Times New Roman', 12, 'bold'))
#label2.pack()
label2.place(x=80, y=140)

# button widget
'''the function to call predictor app, which is going to assigned to the button.'''
def CallingPredictor():
    global process
    #process = Popen("/home/samir/git/master_thesis_project1/6.Gui_2.py", shell=True)
    #subprocess.call("/home/samir/git/master_thesis_project1/OpenCV_v1_4.py", shell=True)
    os.system('python3 OpenCV_v_1_4_test.py &')
    #process = os.getpid()
    #print('Process ID:', process)

button_scan = tkinter.Button(window,text="Start Gesture Scan", fg='blue', bg='white',
                             font=('Times New Roman', 10, 'bold'), bd=5,
                             command=CallingPredictor)
button_scan.place(x=110, y=80)
#button_scan.pack()

# second button widget
'''the function to kill predictor app, which is going to assigned to the second button.'''
def KillingPredictor():
    #cam_capture.release()
    #cv2.destroyAllWindows()
    os.kill(process, signal.SIGCONT)

button_scan = tkinter.Button(window,text="Stop Gesture Scan", fg='blue', bg='white',
                             font=('Times New Roman', 10, 'bold'), bd=5,
                             command=KillingPredictor)
button_scan.place(x=110, y=160)
#button_scan.pack()


window.lift()

window.mainloop()
