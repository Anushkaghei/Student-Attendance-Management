import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from functools import partial
import smtplib
import matplotlib.pyplot as plt
import csv
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root=tk.Tk()
root.geometry("1600x800+0+0")
root.title("Attendance Management System")

def rec(option1,option2):
    master=tk.Tk() 
    master.title('Parent-Teacher Communication')
    master.geometry("500x500")
    master.config(bg="aqua")
    
    def send():
        try:
            username=teachers[temp_username.get()]
            password=passwordEntry.get()
            to=students[variable.get()]
            subject=subjectEntry.get()
            body=BodyEntry.get()
            
            if (username=="" or password=="" or to=="" or body==""):
                notif.config(text='All fields required',fg="red",bg="aqua")
                return
            
            else:
                finalMessage='Subject: {}\n\n{}'.format(subject,body)
                server=smtplib.SMTP('smtp.gmail.com',587)#initialising the server/module
                server.starttls()
                server.login(username,password)
                server.sendmail(username,to,finalMessage)
                notif.config(text='Email has been sent',fg='green',bg="aqua")
       
        except:
            notif.config(text='Error sending email',fg="red",bg="aqua")

    def reset():
        usernameEntry.delete(0,'end')
        passwordEntry.delete(0,'end')
        receiverEntry.delete(0,'end')
        subjectEntry.delete(0,'end')
        BodyEntry.delete(0,'end')
        
        
    tk.Label(master,text="Parent-Teacher Communication",font=("Calibri",15),bg="aqua").grid()
    tk.Label(master,bg="aqua").grid(row=1,sticky=tk.W,padx=5)
    
    
    tk.Label(master,text="Email(from):",font=('Calibri',11),bg="aqua").grid(row=2,sticky=tk.W,padx=5)
    tk.Label(master,text="Password:",font=('Calibri',11),bg="aqua").grid(row=4,sticky=tk.W,padx=5)
    tk.Label(master,text="To :",font=("Calibri",11),bg="aqua").grid(row=6,sticky=tk.W,padx=5)
    tk.Label(master,text="Subject:",font=("Calibri",11),bg="aqua").grid(row=8,sticky=tk.W,padx=5)
    tk.Label(master,text="Body:",font=("Calibri",11),bg="aqua").grid(row=10,sticky=tk.W,padx=5)

    notif=tk.Label(master,text="",font=('Calibri',11),bg="aqua")
    notif.grid(row=15,sticky=tk.S,padx=5)

    #storage for entry
    temp_username=tk.StringVar()
    temp_password=tk.StringVar()
    variable=tk.StringVar()
    temp_subject=tk.StringVar()
    temp_body=tk.StringVar()
    
       
    #entries
    usernameEntry=tk.OptionMenu(master,temp_username,*option1.keys())
    usernameEntry.grid(row=2,column=0,padx=90)
    tk.Label(master,bg="aqua").grid(row=3)

    passwordEntry=tk.Entry(master,width=30,show="*",textvariable=temp_password)
    passwordEntry.grid(row=4,column=0,padx=90)
    tk.Label(master,bg="aqua").grid(row=5)

    receiverEntry=tk.OptionMenu(master,variable,*option2.keys())
    receiverEntry.grid(row=6,column=0,padx=90)
    tk.Label(master,bg="aqua").grid(row=7)

    subjectEntry=tk.Entry(master,width=30,textvariable=temp_subject)
    subjectEntry.grid(row=8,column=0,padx=90)
    tk.Label(master,bg="aqua").grid(row=9)

    BodyEntry=tk.Entry(master,width=30,textvariable=temp_body)
    BodyEntry.grid(row=10,column=0,padx=90)
    tk.Label(master,bg="aqua").grid(row=11)

    tk.Button(master,text="Send",command=send).grid(row=14,sticky=tk.W,pady=15,padx=100)
    tk.Button(master,text="Reset",command=reset).grid(row=14,sticky=tk.W,pady=45,padx=200)

    master.mainloop()
    
def Admin():
    win = tk.Tk()
    # Set the size of the window
    win.geometry("1000x800")
    win.title("Administrator")    
    def submit():
        p = entry.get()
        if(str(p)=="admin"):
        
            def openFile():
                tf = filedialog.askopenfilename(
                    initialdir="C:/Users/MainFrame/Desktop/", 
                    title="Open Text file", 
                    filetypes=(("CSV", "*.csv"),)
                    )
                pathh.insert(tk.END, tf)
                tf = open(tf, 'r')
                data = tf.read()
                txtarea.insert(tk.END, data)
                tf.close()
        
            ws = tk.Tk()
            ws.title("Attendance list")
            ws.geometry("400x450+350+150")
            ws['bg']='blue'
        
            txtarea = tk.Text(ws, width=40, height=20)
            txtarea.pack(pady=20)
        
            pathh = tk.Entry(ws)
            pathh.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)
              
            tk.Button(ws, text="Open File", 
                    command=openFile).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=20)
               
            ws.mainloop()

        else:
            tk.Label(win,text="Incorrect password.Retry!").pack()
            
    def check():
        frame2=tk.Frame(win,height=100,width=800)
        tk.Button(frame2,text="send an email",bg="light green",command=partial(rec,teachers,students)).pack(side=tk.LEFT,padx=50)
        tk.Button(frame2,text="open attendance list",width=25,
                  bg="light blue",command=submit).pack(side=tk.RIGHT)
        frame2.pack(side=tk.TOP)
        
        frame1=tk.Frame(win,height=300,width=300)
        x = []
        y = []
          
        with open('attendance.csv','r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                x.append(row[3])
                y.append(row[0])
        x=x[1:] 
        y=y[1:] 
        fig1 = plt.figure(figsize =(7,7))
        plt.plot(x, y, color = 'g', linestyle = 'dashed',
                  marker = 'o',label = "Attendence data by date")
          
        plt.xticks(rotation = 25)
        plt.xlabel('Dates')
        plt.ylabel('Attendence')
        plt.title('Attendence per day', fontsize = 20)
        canvas1 = FigureCanvasTkAgg(fig1,frame1) 
        canvas1.get_tk_widget().pack()
        plt.grid()
        plt.legend()
        frame1.pack(side=tk.RIGHT)
        
        outfile = open("attendance.csv","r", encoding='utf-8')
        file=csv.reader(outfile)
        next(file, None)
        frame=tk.Frame(win,height=300,width=300)        
        name = []
        for row in file:
            name.append(row[1])
        counts = Counter(name[::-1])        
        fig = plt.figure(figsize =(7,7)) 
        plt.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%',normalize=True)
        canvas = FigureCanvasTkAgg(fig,frame) 
        canvas.get_tk_widget().pack()                
        frame.pack(side=tk.LEFT)
        outfile.close()
        
    # Add an Entry widget for accepting User Password
    entry = tk.Entry(win,width=25,show="*")    
    entry.pack(pady=10)
    tk.Button(win, text="Submit", command=check).pack()
    tk.Label(win).pack()
    tk.Label(win).pack
    win.mainloop()	

def record(v):
    path='images'
    images=[]
    personName=[]
    myList=os.listdir(path)

    for cu_img in myList:
        current_Img=cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personName.append(os.path.splitext(cu_img)[0])

    #encoding= dlib module encodes our face with 128 diff features(unique pts)
    def faceEncodings(images):
        encodeList=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    enc=faceEncodings(images)

    def attendance(name):
        b=v.get()
        with open('attendance.csv','r+') as f:
            myDataList=f.readlines()
            nameList=[]
            for line in myDataList:
                entry=line.split(',')
                nameList.append(entry[0])
                
            if name not in nameList:
                time_now=datetime.now()
                tstr=time_now.strftime('%H:%M:%S')#time string
                dstr=time_now.strftime('%d/%m/%Y')#date string
                f.write(f'{b},{name},{tstr},{dstr}\n')
            
    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        faces=cv2.resize(frame,(0,0),None,0.25,0.25)
        faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
        
        facesCurrentFrame=face_recognition.face_locations(faces)
        encodesCurrentFrame=face_recognition.face_encodings(faces,facesCurrentFrame)
        
        for encodeFace, faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
            matches=face_recognition.compare_faces(enc,encodeFace)
            faceDis=face_recognition.face_distance(enc,encodeFace)
            
            matchIndex=np.argmin(faceDis)#gives index value of min distance
            
            if matches[matchIndex]:
                name=personName[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                
                attendance(name)
        
        cv2.imshow("Camera",frame)
        if cv2.waitKey(7000)==13: #13 is the ascii code for enter
               break
    cap.release()
    cv2.destroyAllWindows()
                  
def student():
    window=tk.Toplevel()
    window.geometry("400x400+0+0")
    window.config(bg="aqua")
    global v1,v2,v3,v4,v5
    def check():
        s = entry.get()
        if(str(s)=="admin"): 
            
            tk.Label(window, 
                     text="Subject:-",
                     justify = tk.LEFT,
                     bg="aqua",
                     padx = 20).pack(anchor=tk.W)
            
            
            v1 = tk.StringVar()
            tk.Radiobutton(window, 
                           text="Computer science",
                           padx = 20, 
                           variable=v1, 
                           value="CS",
                           bg="aqua",
                           command=partial(record,v1)).pack(anchor=tk.W)
            
            v2 = tk.StringVar()
            tk.Radiobutton(window, 
                           text="Engineering Chemistry",
                           padx = 20, 
                           variable=v2, 
                           value="CHEM",
                           bg="aqua",
                           command=partial(record,v2)).pack(anchor=tk.W)
                
            v3 = tk.StringVar()
            tk.Radiobutton(window, 
                           text="Engineering Mathematics",
                           padx = 20, 
                           variable=v3, 
                           value="MATHS",
                           bg="aqua",
                           command=partial(record,v3)).pack(anchor=tk.W)
            
            v4= tk.StringVar()
            tk.Radiobutton(window, 
                           text="Engineering Mechanics",
                           padx = 20, 
                           variable=v4, 
                           value="MECH",
                           bg="aqua",
                           command=partial(record,v4)).pack(anchor=tk.W)
            
            v5= tk.StringVar()
            tk.Radiobutton(window, 
                           text="Electronic Principles and Devices",
                           padx = 20, 
                           variable=v5, 
                           value="EPD",
                           bg="aqua",
                           command=partial(record,v5)).pack(anchor=tk.W)    
    
    entry = tk.Entry(window,width=25,show="*")    
    entry.pack(pady=10)
    tk.Button(window, text="Submit", command=check).pack()
    tk.Label(window,bg="aqua").pack()
    tk.Label(window,bg="aqua").pack            
    window.mainloop()																																					
        

frame=tk.Frame(root,height=800,width=600)
frame.configure(background="blue")
tk.Label(frame,bg="blue").pack()

photo=tk.PhotoImage(file="logo.gif")
l=tk.Label(frame,image=photo).pack()
tk.Label(frame,bg="blue").pack()
tk.Label(frame,bg="blue").pack()

photo2=tk.PhotoImage(file="class.gif")
l=tk.Label(root,image=photo2).pack(side=tk.RIGHT)

l1=tk.Label(frame,text="Sign in",fg="black",bg="blue",font=('Ariel',30)).pack()
tk.Label(frame,bg="blue").pack()
tk.Label(frame,bg="blue").pack()

tk.Button(frame,text="Administrator",width=12,command=Admin,font=('Ariel',22)).pack()
tk.Label(frame,bg="blue").pack()

tk.Button(frame,text="Student",width=12,font=('Ariel',22),command=student).pack()
tk.Label(frame,bg="blue").pack()

tk.Button(frame,text="Parent",width=12,font=('Ariel',22),command=partial(rec,students,teachers)).pack()

frame.pack_propagate(False)
frame.pack(fill="both",side=tk.LEFT)
root.mainloop()
