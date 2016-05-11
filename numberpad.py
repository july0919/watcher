#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

mode = "1"
password = "1234"
change_password = ""
yes_number = ""
star = ""

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

def change_press(widget):
    global mode, star, yes_number
    mode = "2"
    yes_number = ""
    star = ""
    entry.set_text("")

def cancel_press(widget):
    global mode, star, yes_number, change_password
    change_password = ""
    yes_number = ""
    star = ""
    entry.set_text("")
    if mode == "2":
        mode = "1"

def yes_press(widget):
    global mode, star, password, yes_number, change_password
    if mode == "1":
        if password == yes_number:
            print(yes_number)
        yes_number = ""
        star = ""
        entry.set_text("")
    if mode == "2":
        password = change_password
        change_password = ""
        star = ""
        entry.set_text("")
        mode = "1"


win = gtk.Window()
win.connect('destroy', lambda w: gtk.main_quit())

box = gtk.VBox()
win.add(box)

pix = gtk.gdk.pixbuf_new_from_file("/home/pi/Pictures/Tux")
pix = pix.scale_simple(200, 200, gtk.gdk.INTERP_BILINEAR)
image = gtk.image_new_from_pixbuf(pix)
box3 = gtk.VBox()
box3.pack_start(image)
box.pack_start(box3)

entry = gtk.Entry()
box.pack_start(entry, False)

table = gtk.Table(2,2, gtk.TRUE)

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, "#", 0, "*"]
x = 0
y = 0

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
