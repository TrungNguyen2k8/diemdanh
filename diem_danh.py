from tkinter import *
import time, threading, os # type: ignore
from tkinter import messagebox as msb
import cv2
import pyzbar
import pyzbar.pyzbar

capture = cv2.VideoCapture(0)
FONT = [('Arial',48,'bold'), ('Arial',28), ('Arial',24)]
classlist = [8,9,10,11,12]
dslop = {}
dau = ","

def create_diemdanh_folder():
    try:
        if not os.path.isdir(f"./diemdanh_T{month}_{year}"):
            os.mkdir(f"./diemdanh_T{month}_{year}")
        
        if not os.path.isdir(f"./diemdanh_T{month}_{year}/{day}.{month}.{year}"):
            os.mkdir(f"./diemdanh_T{month}_{year}/{day}.{month}.{year}")
            
        if not os.path.isdir("./diemdanh_new"):
            os.mkdir("./diemdanh_new")
            
        with open(f"./diemdanh_new/{year}.{month}.{day}.csv", "w",encoding='utf-8') as f:
            f.write("sep="+dau+"\n")
            f.write("ID{0}Class{0}Name{0}Phone{0}Parent's phone{0}Attended\n".format(dau))
            for i in range(1, 999):
                if i in dslop:
                    data = dslop.get(i)
                    f.write(f"{i}{dau}{data[0]}{dau}{data[1]}{dau}{data[2]}{dau}{data[3]}{dau}\n")

    except:
        retry = msb.askretrycancel("Error", "Denied")
        create_diemdanh_folder() if retry else quit()

def readfile():
    try:
        for i in classlist:
            with open(f"./class/{i}.csv", encoding='utf-8') as f:
                if "sep=" in f.readline():
                    f.readline()
                    
                for line in f:
                    li = line.split(dau)
                    if "." in li[0]:
                        dautp = "."
                    else:
                        dautp = ","
                    cl = int(li[0].split(dautp)[0])
                    id_ = int(li[0].split(dautp)[1])
                    name_ = raau(li[1])
                    phone_ = li[2] if len(li[2])==10 else "0"+ li[2]
                    pphone_ = li[3][:-1] if len(li[3][:-1])==10 else "0"+ li[3][:-1]
                    while id_<100 and cl!=classlist[0]: id_ *= 10
                    dslop.update({id_ : [cl, name_, phone_, pphone_]})
    except:
        retry = msb.askretrycancel("Error", "Fail to read file")
        readfile() if retry else quit()
                             
def raau(s):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮ\
        ắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAa\
        AaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    str_ = ''
    for i in s:
        if i in s1:
            str_ += s0[s1.index(i)]
        else:
            str_ += i
            
    return str_.upper()

def clock():
    try:
        global lctime
        
        while True:
            lctime = time.localtime()
            tmstr = time.strftime('%A %d/%m/%Y %H:%M',lctime)
            t.set(tmstr)
            root.update()
            if day != time.localtime().tm_mday:
                first_procedure()
            
            if len(id.get()) == 3:
                check()
            else:
                name.set("")
                phone.set("")
            
            frame = capture.read()[1]
            
            if qrcheck.get():
                
                qr = pyzbar.pyzbar.decode(frame)
                if qr != [] and id.get() == "":
                    kq = int(str(qr[0][0])[2:-1])
                    id.insert(0,kq)
                    check()
                    time.sleep(0.5)
                    diemdanh()
                    time.sleep(0.4)
            
    except:
        clock()
    
def timer():
    time.sleep(0.6)
    resultlb.config(fg='black')
    resultlb.config(fg="black", text="")
    
def diemdanh(*args):
    try: 
        id_ = int(id.get())
    except:
        return
    
    if dslop.get(id_) == None:
        id.delete(0,END)
        return
    
    data = dslop.get(id_)
    cl_ = data[0]
    
    if not os.path.exists(f"./diemdanh_T{month}_{year}/{day}.{month}.{year}/{cl_}.csv"):          
        with open(f"./diemdanh_T{month}_{year}/{day}.{month}.{year}/{cl_}.csv", "w", encoding='utf-8') as f:
            f.write("sep="+dau+"\n")
            f.write("ID{0}Name{0}Phone{0}Parent's phone{0}Attended\n".format(dau))
            
            for key in dslop.keys():
                data_ = dslop.get(key)
                if data_[0] == cl_:
                    f.write("{0},{1},{2},{3},\n".format(key,data_[1],data_[2],data_[3]))
                    
            f.close()

    try:
        save_to_file(cl_, id_)
        resultlb.config(fg="green", text="Success")
        threading.Thread(target=timer, daemon=True).start()
        
        id.delete(0,END)
        name.set("")
        phone.set("")
        
    except:
        resultlb.config(fg="red", text="Error")
    
def check():
    try:
        id_ = int(id.get())
        data = dslop.get(id_)
        name_ = data[1]
        phone_ = data[2]
        name.set(name_)
        phone.set(phone_)
    except:
        name.set("none")
   
def save_to_file(cl, id):
    newtext = []
    with open(f"./diemdanh_T{month}_{year}/{day}.{month}.{year}/{cl}.csv", encoding='utf-8') as f:
        if 'sep=' in f.readline():
            f.readline()
            
        for line in f:
            data = line.split(dau)
            id_ = int(data[0])
            if id_ == id:
                data.pop()
                data.append(f"{time.strftime('%H:%M',lctime)}\n")
            newtext.append(dau.join(data))
        f.close()
        
    with open(f"./diemdanh_T{month}_{year}/{day}.{month}.{year}/{cl}.csv", "w",encoding='utf-8') as f:
        f.write("sep="+dau+"\n")
        f.write("ID{0}Name{0}Phone{0}Parent's phone{0}Attended\n".format(dau))
        for i in newtext:
            f.write(i)
        f.close()
        
    newtext.clear()
    with open(f"./diemdanh_new/{year}.{month}.{day}.csv", "r",encoding='utf-8') as f:
        if 'sep=' in f.readline():
            f.readline()
        for line in f:
            data = line.split(dau)
            if int(data[0]) == id:
                data.pop()
                data.append(f"{time.strftime('%H:%M',lctime)}\n")
            newtext.append(dau.join(data))
        f.close()
            
    with open(f"./diemdanh_new/{year}.{month}.{day}.csv", "w",encoding='utf-8') as f:
        f.write("sep="+dau+"\n")
        f.write("ID{0}Class{0}Name{0}Phone{0}Parent's phone{0}Attended\n".format(dau))
        for i in newtext:
            f.write(i)
        f.close()
    
    global checked
    checked = False

def forgetid():
    def find_student():
        student = [int(cl.get()), raau(n.get()), pn.get()]
        for key in dslop.keys():
            if student[0] == dslop.get(key)[0] and student[1] == dslop.get(key)[1] and \
            (student[2] == dslop.get(key)[2] or "0"+student[2] == dslop.get(key)[2] or student[2] == "0"+dslop.get(key)[2]):
                msb.showinfo("Student found", f"Your ID is {key}\nRemember it!")
                save_to_file(int(cl.get()), key)
                return
        msb.showwarning("Not found", "Student not found!\nIf you haven't had the ID yet, please click 'No ID?' or 'Reset'")
    
    try:
        w = Toplevel(root)
        
        Label(w, text='Your class', font=FONT[2]).grid(row=0,column=0,padx=5,pady=5,sticky='e')
        cl = Entry(w, font=FONT[1], relief=SOLID,width=30)
        cl.grid(row=0,column=1,padx=5,pady=5,ipady=5)
        
        Label(w, text='Your name', font=FONT[2]).grid(row=1,column=0,padx=5,pady=5,sticky='e')
        n = Entry(w, font=FONT[1], relief=SOLID,width=30)
        n.grid(row=1,column=1,padx=5,pady=5,ipady=5)
        
        Label(w, text='Phone', font=FONT[2]).grid(row=3,column=0,padx=5,pady=5,sticky='e')
        pn = Entry(w, font=FONT[1], relief=SOLID,width=30)
        pn.grid(row=3,column=1,padx=5,pady=5,ipady=5)
        
        Button(w, text="SUBMIT", font=FONT[2], command=find_student, relief=SOLID, bg='light blue').grid(row=5,column=0,\
            columnspan=2,padx=5,pady=5)
        
        w.mainloop()
        
    except:
        pass
    
def openfolder():
    first_procedure()
    path = os.getcwd()
    os.startfile(f"{path}/diemdanh_T{month}_{year}/{day}.{month}.{year}")

def first_procedure():
    global month, year, day
    month = time.localtime().tm_mon
    year = time.localtime().tm_year
    day = time.localtime().tm_mday
    
    readfile()
    create_diemdanh_folder()
    
#Main programe------------------------------------------------------------------------------------------------------
first_procedure()

root = Tk()
root.state('zoomed')
root.title("Attendance Software")

icon = PhotoImage(file="./media/icon.png")
root.iconphoto(True, icon)

#Some variables------------------------------------
name = StringVar()
phone = StringVar()
t = StringVar()
qrcheck = BooleanVar()

qrcheck.set("True")

#Binding-------------------------------------------    
root.bind("<Return>", diemdanh)

#--------------------------------------------------
main = Frame(root)
main.pack(expand=True)

#Title--------------------------------
Label(main, text = 'Attendance', font = FONT[0]).pack(pady=10)

#Class/QR---------------------------

options = Frame(main)
options.pack(pady=10)

reseticon = PhotoImage(master=options, file='./media/circular.png')

Label(options, text = 'Class', font = FONT[1]).pack(side=LEFT)
Button(options, image=reseticon, command=first_procedure).pack(side=LEFT)

Checkbutton(options, text="QR check",compound=LEFT, font=FONT[1],\
    variable=qrcheck,onvalue=True,offvalue=False).pack(side=RIGHT, padx=40)

#--------------------------------------
main1 = Frame(main,pady=10)
main1.pack(anchor='w',padx=20)

#ID------------------------------------
Label(main1, font = FONT[1], text = 'ID').grid(row=0,column=0,sticky=E, padx=5)

id = Entry(main1, font=FONT[1],relief=SOLID,width=10, bg = 'white', justify=CENTER)
id.grid(row=0,column=1,sticky=NSEW, padx=5)

#Enter---------------------------------
Button(main1, text = "Enter", font = FONT[2], relief=SOLID, bg = 'dark green', \
    fg = 'white', width = 6, command = diemdanh).grid(row=0,column=2, padx=5)

#Forget ID-----------------------------
Button(main1, text="Forget ID?", font = FONT[2], relief=SOLID, fg = 'blue', bg='yellow', command=forgetid).grid(row=0, column=3)

#--------------------------------------
Button(main1, text="Atd folder", font = FONT[2], relief=SOLID, fg = 'black', bg='yellow', command=openfolder).grid(row=0, column=4)

#Name, Phone---------------------------
Label(main1, text='Name', font=FONT[1]).grid(row=1,column=0, pady=20, padx=5)
Label(main1, textvariable=name, font = FONT[2],fg='blue',width=28, bg='white',relief=SOLID).grid(row=1,column=1, padx=5, columnspan=2)
Label(main1, text="Phone", font=FONT[1]).grid(row=1,column=3, padx=5)
Label(main1, font=FONT[2], width=11, bg= 'white', textvariable=phone,relief=SOLID).grid(row=1,column=4, padx=5)

#Result--------------------------------
resultlb = Label(main, font = FONT[1], width=10)
resultlb.pack(pady=5)

#Clock---------------------------------
Label(main, textvariable= t, font=FONT[2]).pack(pady=10)
threading.Thread(target=clock, daemon=True).start()

#--------------------------------------
root.mainloop()