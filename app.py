from tkinter import *
from gehuchatbot import *
class chatbot:
    def __init__(self):
        self.speach=True
        self.window=Tk()
        self.mainwindow()
        self.obj=gehu()
    def run(self):
        self.window.mainloop()
        
    def mainwindow(self):
        # Windows title
        self.window.title("Gehu Chatbot")
        self.window.iconbitmap("./data/img/favicon.ico")
        self.window.resizable(width=False,height=False)
        self.window.configure(width="420px",height="500px",bg="#99e6ff")
        
        # Header section 
        header=Label(self.window,bg="#000080",fg="white",text="Welcome to EraGuide",font=("Arial",20,"bold"),pady=12)
        header.place(relwidth=1,relheight=.08)
        
        # Mute/unmute button
        def toogletext(event):
            if(mutebtn['text']=="READ"):
                mutebtn.config(
                    text="MUTE",
                    background="#000080"
                )
            else:
                mutebtn.config(
                    text="READ",
                    background="#000080"
                )
        mutebtn=Button(self.window,text="MUTE",font=("Arial",14),
                       command=lambda: self.togglespeach(),background="#000080",foreground="white",highlightthickness=2,highlightbackground="#ff1a1a",
                       highlightcolor="white",
                       activebackground="white",
                       activeforeground="black",
                       cursor="hand1",
                        borderwidth=2,
                        relief="ridge"
                       )
        mutebtn.place(relheight=.06,relwidth=.14,relx=.84,rely=.01)
        mutebtn.bind('<Button-1>',toogletext)
        def btn_enter(event):
            mutebtn.config(
                highlightbackground="#ff4d94"
            )
        def btn_leave(event):
            mutebtn.config(
                highlightbackground="#ff0066"
            )
        mutebtn.bind("<Enter>",btn_enter)
        mutebtn.bind("<Leave>",btn_leave)
        
        # partition
        line=Label(self.window,bg="white")
        line.place(relwidth=1,rely=.085,relheight=.006)
        
        # Textarea
        self.textarea=Text(self.window,width=5,bg="#F0F8FF",fg="black",font=("Roboto",14,"bold"),pady=5,padx=8)
        self.textarea.place(relheight=.8,relwidth=.98,relx=.01,rely=.097)
        self.textarea.configure(cursor="arrow",state=DISABLED)
        
        scroll_bar=Scrollbar(self.window)
        scroll_bar.place(relheight=.8,relx=.98,rely=.097,relwidth=.02)
        scroll_bar.configure(command=self.textarea.yview)
        
        # Bottom section
        bottom=Label(self.window,bg="#00008B")
        bottom.place(relheight=.09,relwidth=.98,rely=.9,relx=.01)
        
        self.userreq=Entry(bottom,bg="white",fg="black",font=("Roboto",16))
        self.userreq.place(relheight=.8,relwidth=.8,rely=.1,relx=.01)
        self.userreq.focus()
        self.userreq.bind("<Return>",self.onEnter)
        
        sendbtn=Button(bottom,text="Send",bg="#000080",fg="white",font=("Arial",16,"bold"),command=lambda:self.onEnter(None))
        sendbtn.place(relheight=.8,relwidth=.18,rely=.1,relx=.82)
    
    def onEnter(self,event):
        msg=self.userreq.get()
        self.insertToTextarea(msg)
        
    def type(self,counter=0):
        if(counter==len(self.botmsg)):
            self.textarea.configure(state=DISABLED)
            return
        self.textarea.insert(END,self.botmsg[counter])
        if(self.botmsg[counter]=='\n'):
            self.textarea.see(END)
        self.window.after(50, lambda: self.type(counter+1))
            
    def insertToTextarea(self,msg):
        if(msg==""):
            return 
        self.userreq.delete(0,END)
        msg1=f"You : {msg}\n\n"
        self.textarea.configure(state=NORMAL)
        self.textarea.insert(END,msg1)
        self.textarea.configure(state=DISABLED)
        generatedmsg=self.obj.generateres(msg)
        msg2=f"Bot : {generatedmsg}\n\n"
        self.textarea.configure(state=NORMAL)
        self.botmsg=msg2
        self.type()
        self.textarea.see(END)
        if(self.speach==True):
            self.obj.speaktheoutput()
    def togglespeach(self):
        if(self.speach==True):
            self.speach=False
        else:
            self.speach=True
app=chatbot()
app.run()