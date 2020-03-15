# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# udpcli1.py: simplest client program
#
# Gets a string from the user, has a server process it, prints the result
#
from socket import socket, AF_INET, SOCK_DGRAM
from Tkinter import *
win=Tk()
win.title(u"嵌入式系統專題")
srvaddr = ('192.168.7.2', 11111)      # server address
s = socket(AF_INET, SOCK_DGRAM)     # create a socket
s.bind(('', 0))

def click1():
	s.sendto("1", srvaddr)
def click2():
	s.sendto("2", srvaddr)
def click3():
	s.sendto("3", srvaddr)
def click4():
	s.sendto("4", srvaddr)
def click5():
	s.sendto("5", srvaddr)
def click6():
	s.sendto("6", srvaddr)
def click7():
	s.sendto("7", srvaddr)
def click8():
	s.sendto("8", srvaddr)
def click9():
	s.sendto("9", srvaddr)
def click10():
	s.sendto("10", srvaddr)
def click11():
	s.sendto("11", srvaddr)
def click12():
	s.sendto("12", srvaddr)
def click13():
	s.sendto("13", srvaddr)
def click14():
	s.sendto("14", srvaddr)
def click15():
	s.sendto("15", srvaddr)
def click16():
	s.sendto("16", srvaddr)


button1=Button(win, text=u"紅燈恆亮", command=click1)
button2=Button(win, text=u"綠燈恆亮", command=click2)
button3=Button(win, text=u"黃燈恆亮", command=click3)
button4=Button(win, text=u"紅燈閃爍", command=click4)
button5=Button(win, text=u"綠燈閃爍", command=click5)
button6=Button(win, text=u"黃燈閃爍", command=click6)
button7=Button(win, text=u"紅燈關閉", command=click7)
button8=Button(win, text=u"綠燈關閉", command=click8)
button9=Button(win, text=u"黃燈關閉", command=click9)
button10=Button(win, text=u"全部開啟", command=click10)
button11=Button(win, text=u"全部關閉", command=click11)
button12=Button(win, text=u"輪流閃爍", command=click12)
button13=Button(win, text=u"同時閃爍", command=click13)
button14=Button(win, text=u"顯示溫度", command=click14)
button15=Button(win, text=u"顯示時間", command=click16)
button16=Button(win, text=u"語音辨識", command=click15)

button1.grid(row=0,column=0,sticky = W)
button2.grid(row=1,column=0,sticky = W)
button3.grid(row=2,column=0,sticky = W)
button4.grid(row=0,column=2,sticky = W)
button5.grid(row=1,column=2,sticky = W)
button6.grid(row=2,column=2,sticky = W)
button7.grid(row=0,column=4,sticky = W)
button8.grid(row=1,column=4,sticky = W)
button9.grid(row=2,column=4,sticky = W)
button10.grid(row=3,column=1,sticky = W)
button11.grid(row=3,column=3,sticky = W)
button12.grid(row=4,column=0,sticky = W)
button13.grid(row=4,column=2,sticky = W)
button14.grid(row=5,column=2,sticky = W)
button15.grid(row=5,column=3,sticky = W)
button16.grid(row=5,column=4,sticky = W)

win.mainloop()