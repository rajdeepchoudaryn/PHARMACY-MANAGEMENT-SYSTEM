def p(event):
             global cal,dw
             dw=Toplevel()
             dw.grab_set()
             dw.title("6y")
             dw.geometry('250x220+590+370')
                        
             cal=Calendar(dw,selectmode='day',date_pattern='dd/mm/y')
             cal.place(x=0,y=0)

             sb=Button(dw,text="select",command=g)
             sb.place(x=90,y=190)
        def g():
             global wox
             today = date.today()
             y = today.year
             m = today.month
             d = today.day
             wox=f"{d}/{m}/{y}"
             d1=datetime.strptime(wox,"%d/%m/%Y")
             d2=datetime.strptime(cal.get_date(),"%d/%m/%Y")
             result=d2-d1
             if result.days<0:
                  dw.destroy()
                  messagebox.showerror("showerror","Please enter correct date!")
             else:
                  pa.insert(0,wox)
                  dw.destroy()
