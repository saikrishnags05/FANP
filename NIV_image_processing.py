import numpy as np
import cv2
import  imutils 
import sys
import sqlite3
import pytesseract
import time
import datetime
import pyttsx3
from tkinter import *
from tkinter import messagebox
import os
import numpy as np
from tkinter import filedialog
root =Tk()
root.withdraw()
i=0
try:
    if not os.path.exists('image_face_detection'):
        os.makedirs('image_face_detection')
except OSError:
    i=i+1
    s='image_face_detection'+str(i)
    os.makedirs(s)
try:
    if not os.path.exists('video_face_detection'):
        os.makedirs('video_face_detection')
except OSError:
    print ('Error: Creating directory of data')
ARIAL = ("arial",10,"bold")
ARIAL = ("arial",10,"bold")
class main_frame:
    def __init__(self,root):

            self.root = root
            self.header = Label(root,text="IMAGE PROCESSING",bg="#50A8B0",fg="white",font=("arial",30,"bold"))
            self.header.pack(fill=X)
            self.new_acc=Button(root,text="NUMBER PLATE READER",bg="#50A8B0",fg="white",font=ARIAL,command=get_plate).place(x=200,y=115,width=200,height=50)
            self.login_button= Button(root,text="FACE IDENTIFACTION",bg="#50A8B0",fg="white",font=ARIAL,command= get_face).place(x=200, y=215, width=200, height=50)
            self.admin_btton= Button(root,text="VIDEO FACE DETECTER",bg="#50A8B0",fg="white",font=ARIAL,command=video_get_face).place(x=200, y=315, width=200, height=50)
            

            
            self.engine = pyttsx3.init()
            #self.engine.setProperty('rate', 150)    # Speed percent (can go over 100)
            #self.engine.setProperty('volume', 0.9)
            self.engine.say("Wellcome to main menu of image processing !")
            self.engine.say("Please select any option by clicking on it")
            self.engine.runAndWait()
            self.quit = Button(root, text="Exit", width=20, height=2, command=root.destroy, bg='#EE3D3D').place(x=200,y=415)
class face_ditect:
    def __init__(self):
        self.currdir = os.getcwd()
        self.tempdir=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("PNG_file","*.png*")))
        if len(self.tempdir) > 0:
            self.imagePath = self.tempdir      
        self.image =cv2.imread(self.imagePath)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faceCascade =cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.faces = self.faceCascade.detectMultiScale(self.gray,scaleFactor=1.1,minNeighbors=3,minSize=(30, 30))
        self.currentFrame=0
        for (self.x, self.y, self.w, self.h) in self.faces:
                cv2.rectangle(self.image, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)
                self.roi_color = self.image[self.y:self.y + self.h, self.x:self.x + self.w]
               #if not self.ret:
                #        break
                self.name = './image_face_detection/frame' + str(self.currentFrame) + '.jpg'
                #print ('Creating...' + self.name)
                cv2.imwrite(self.name, self.roi_color)
                self.currentFrame += 1
                #cv2.imwrite(str(self.w) + str(self.h) + '_faces.jpg', self.roi_color)
        self.co1=len(self.faces)
        s=str(self.co1)+" "+"are identified please check in the folder"
        messagebox.showinfo("Success", s)
        self.co="total" + " "+ str(self.co1)+" " + "are identified please check in then folder"
        self.engine1 = pyttsx3.init()
        self.engine1.say(self.co)
        self.engine1.runAndWait()
class video_face_ditect:
    def __init__(self):
        self.currdir = os.getcwd()
        self.tempdir=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("MP4_video","*.mp4*"),("AVI_video","*.avi*"),("MOV_video","*.MOV*")))
        if len(self.tempdir) > 0:
            self.imagePath = self.tempdir
        self.cap = cv2.VideoCapture(self.tempdir)
        self.face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.currentFrame=0
        try:
            while(True):
                self.ret, self.frame = self.cap.read()
                self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.faces=self.face_cascade.detectMultiScale(self.gray,1.3,5)
                for(self.x,self.y,self.w,self.h) in self.faces:
                    cv2.rectangle(self.frame,(self.x,self.y),(self.x+self.w,self.y+self.h),(0,255,0),2)
                    self.roi_color =self.frame[self.y:self.y + self.h,self.x:self.x + self.w]
                    #if not self.ret:
                     #   break
                    self.name = './video_face_detection/frame' + str(self.currentFrame) + '.jpg'
                    #print ('Creating...' + self.name)
                    cv2.imwrite(self.name, self.roi_color)
                    self.currentFrame += 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            self.cap.release()
            cv2.destroyAllWindows()
        except:
            s=str(self.currentFrame)+" "+"are identified please check in the folder"
            messagebox.showinfo("Success", s)
           

        
class number_plate_reader:
     def __init__(self):
        self.currdir = os.getcwd()
        self.tempdir=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpg files","*.jpg"),("PNG_file","*.png*"),("jpeg files","*.JPEG")))
        if len(self.tempdir) > 0:
            self.imagePath = self.tempdir
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        self.image = cv2.imread(self.imagePath)
        self.image = imutils.resize(self.image, width=500)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.gray = cv2.bilateralFilter(self.gray, 11, 17, 17)
        self.edged = cv2.Canny(self.gray, 170, 200)
        (cnts, _) = cv2.findContours(self.edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
        self.NumberPlateCnt = None 
        self.count = 0
        for self.c in self.cnts:
                self.peri = cv2.arcLength(self.c, True)
                self.approx = cv2.approxPolyDP(self.c, 0.02 * self.peri, True)
                if len(self.approx) == 4:  
                    self.NumberPlateCnt = self.approx 
                    break
        self.mask = np.zeros(self.gray.shape,np.uint8)
        self.new_image = cv2.drawContours(self.mask,[self.NumberPlateCnt],0,255,-1)
        self.new_image = cv2.bitwise_and(self.image,self.image,mask=self.mask)
        self.config = ('-l eng --oem 1 --psm 3')
        self.text = pytesseract.image_to_string(self.new_image,config=self.config)
        self.acc_list = []
        self.conn = sqlite3.connect('C:\\Users\\SAI KRISHNA\\Desktop\\major_1\\major project\\mj_set\\final_phase_with__individual_gui\\NumberPlate.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS number_plate(plate_id text PRIMARY KEY ,name_of_owner varchar(50), do_of_issue text,vehicle_name varchar(30),vehicle_type varchar(30),vehicle_color varchar(25),city varchar(40),address text, number varchar(10))')
        self.ac=self.text
        self.s=self.text
        self.l=[]
        self.q=1
        self.s1=""
        for i in self.s:
            if self.q<11:
                if i!=' ':
                    self.l.append(i)
                    self.q+=1
        #print(self.l)
        for i in self.l:
            self.s1=self.s1+i
        #print(self.s1)
        self.temp=self.conn.execute("select * from number_plate where plate_id = ? ",(self.s1,))
        #print(self.s1)
        for i in self.temp:
            self.acc_list.append("number plate  {}".format(i[0]))
            self.acc_list.append("OWNER  {}".format(i[1]))
            self.acc_list.append("DATE OF ISSUE {}".format(i[2]))
            self.ac = i[2]
            self.acc_list.append("CAR NAME  {}".format(i[3]))
            self.acc_list.append("CAR TYPE  {}".format(i[4]))
            self.acc_list.append("CAR COLOR  {}".format(i[5]))
            self.acc_list.append("LOCATION {}".format(i[6]))
            self.acc_list.append("ADDRESS  {}".format(i[7]))
            self.acc_list.append("PHONE NUMBER  {}".format(i[8]))
            

        self.tpk = pyttsx3.init()
        self.tpk.say(self.acc_list)
        self.tpk.runAndWait()
        self.root1 = Tk()
        self.scrollbar = Scrollbar(self.root1)
        self.scrollbar.pack( side = RIGHT, fill = Y )
        self.mylist = Listbox(self.root1, yscrollcommand = self.scrollbar.set,height = 10,width =30 )
        self.root1.resizable(False,False)
        for self.line in self.acc_list:
            self.mylist.insert(END,self.line)
        self.mylist.pack( side = LEFT, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )
        self.root1.mainloop()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
   
def get_face():     
    obj = face_ditect()
def video_get_face():     
    obj = video_face_ditect()
def get_plate():     
    obj = number_plate_reader()
def close():
    #root.destroy()
    root.quit()
    
def main_gui():
    
    root = Tk()
    root.title("MENU")
    root.geometry("600x600")
    root.resizable(False,False)
    try:
        root.iconbitmap('icons\\icon.ico')
    except:
        root.iconbitmap('C:\\Users\\SAI KRISHNA\\Desktop\\major project\\mj_set\\final_phase_with__individual_gui\\icons\\icon.ico')
    root.configure( background='#728B8E')
    obj = main_frame(root)
    #q = Button(root,text="Quit",bg="#50A8B0",fg="white",font=ARIAL,command =close).place(x=200, y=415, width=200, height=50)
    root.mainloop()
main_gui()

