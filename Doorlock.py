#!/usr/bin/env python
import numpy as np
import cv2
import time
import datetime
from PIL import Image
import MySQLdb
import serial
import random
import pygtk
pygtk.require('2.0')
import gtk

SerialFromArduino = serial.Serial('/dev/ttyACM0',9600)

now=datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

#Doorlock basic Setting
mode = "1"
password = "1234"
change_password = ""
yes_number = ""
star = ""

#Wait until accessor come
while True:
    input_s = SerialFromArduino.read()
    print input_s
    if input_s == "d":
        break

#Camera ON, Face detect start
def detect(img, cascade):       #face detect
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=3,minSize=(80,80), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:         #if not detected
        return[]
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1 ,y1, x2, y2 in rects:
        cv2.rectangle(img, (x1,y1),(x2,y2),color,2)     #draw rectangle

#If being run standalone: True, If being imported :False
if __name__ == '__main__':
    cascade_fn = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"     #Load function
    nested_fn = "/usr/local/share/OpenCV/haarcascades/haarcascade_eye,xml"
    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)

    cam = cv2.VideoCapture(0)       #Camera setting
    cam.set(3, 320) #width
    cam.set(4, 240) #height

#Face detection start
    while True:
        ret, img = cam.read()
#Convert into gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
#Find Face
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
#Fine Eyes
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2:, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = detect(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255,0,0))
#Mark time
#        timestamp = datetime.datetime.now()
#        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
#        cv2.putText(vis, ts, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0,0,255),1)

#If face detected
        if len(rects) != 0:
            filepath = '/var/www/html/watcher_record/'
            filename = nowDatetime+'.jpg'

            dbpath = 'watcher_record/'+filename
            cv2.imwrite(filepath+filename,vis)     #Save
            db = MySQLdb.connect("localhost","root","zeng1877","watcher")#            cursor = db.cursor()
            cursor = db.cursor()
#            with db:
#                cursor.execute("insert into record values(NOW(),"+filepath+filename+");")
            db.close()
            break;                          #Exit
    cv2.destroyAllWindows()
    time.sleep(2)

## Numberpad Activate
#when press is pushed
def number_press(widget):
    global mode, star, yes_number, change_password
    if mode == "1":
       star += "*"
       entry.set_text(star)
       yes_number += widget.get_label()
    elif mode == "2":
         star += "*"
         entry.set_text(star)
         change_password += widget.get_label()
#if want to change password
def change_press(widget):
    global mode, star, yes_number
    mode = "2"
    yes_number = ""
    star = ""
    entry.set_text("")

#when you cancel during doing something
def cancel_press(widget):
    global mode, star, yes_number, change_password
    change_password = ""
    yes_number = ""
    star = ""
    entry.set_text("")
    if mode == "2":
        mode = "1"

#when you push Yes Button
def yes_press(widget):
    global mode, star, password, yes_number, change_password
    if mode == "1":
        if password == yes_number:
            open_message = 'o'
            SerialFromArduino.write(open_message)
            win.destroy()
        yes_number = ""
        star = ""
        entry.set_text("")
    if mode == "2":
        password = change_password
        change_password = ""
        star = ""
        entry.set_text("")
        mode = "1"

#to declare for using window display
win = gtk.Window()
win.maximize()
win.connect('destroy', lambda w: gtk.main_quit())

#use Vertical Box
box = gtk.VBox()
win.add(box)

#use picture located in a specific file and decide size
pix = gtk.gdk.pixbuf_new_from_file(filepath+filename)
pix = pix.scale_simple(256, 192, gtk.gdk.INTERP_BILINEAR)
image = gtk.image_new_from_pixbuf(pix)
box3 = gtk.VBox()
box3.pack_start(image)
box.pack_start(box3)

entry = gtk.Entry()
box.pack_start(entry, False)
table = gtk.Table(2,2, gtk.TRUE)

#set random numberpad
a = random.sample(range(10),10)
a.insert(9,"*")
a.insert(11,"#")
x = 0
y = 0

#Setting for numberbutton
for i in a:
    button = gtk.Button(str(i))
    button.connect("clicked", number_press)
    table.attach(button, x, x+1, y, y+1)
    x += 1
    if x > 2:
        x = 0
        y += 1
box.pack_start(table)
box2 = gtk.HBox()

#when button is clicked
change = gtk.Button("CHANGE")
change.connect("clicked", change_press)
cancel = gtk.Button("CANCEL")
cancel.connect("clicked", cancel_press)
yes = gtk.Button("YESYES")
yes.connect("clicked", yes_press)
 
box2.pack_start(change)
box2.pack_start(cancel)
box2.pack_start(yes)
box.pack_start(box2)

win.show_all()
gtk.main()

