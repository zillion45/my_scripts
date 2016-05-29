# -*- coding: utf-8 -*-

import os
from Tkinter import *
import ttk
import tkFileDialog
import qrcode
from PIL import Image, ImageTk

PATH = os.path.dirname(os.path.abspath(__file__))

class QrCode:
    def __init__(self, master):
        self.master = master
        self.frame1 = Frame(master, background='white')
        self.frame2 = Frame(master, background='white')
        self.label = Label(self.frame1, text = "Enter the text to create QR Code: ", background='white')
        self.label.pack(side=LEFT)
        self.edit = ttk.Entry(self.frame1)
        self.edit.pack(side=LEFT, fill=BOTH, expand=1)
        self.edit.focus_set()
        self.btn = ttk.Button(self.frame1, text='Generate')
        self.btn.config(command=self.generate_qrcode)
        self.btn.pack(side=LEFT)
        self.frame1.pack(side=TOP, pady=5)
        self.saveas_btn = ttk.Button(self.frame2, text = "Save As...")
        self.saveas_btn.config(command = self.save_img)
        self.saveas_btn.pack(side=LEFT)
        self.exit_btn = ttk.Button(self.frame2, text = "Exit")
        self.exit_btn.config(command = master.quit)
        self.exit_btn.pack(side=RIGHT)
        self.frame2.pack(side=BOTTOM, pady=5)
        self.img = ImageTk.PhotoImage(Image.open("test.png"))
        self.img_label = Label(master, background='white')
        self.img_label.pack(side=TOP, fill=X)


    def generate_qrcode(self):
        self.qr = qrcode.QRCode()
        self.qr.add_data(self.edit.get())
        self.qr.make()
        self.qrimg = self.qr.make_image()

        img = os.path.join(PATH, 'qrcode.png')
        img_file = open(img, 'wb')
        self.qrimg.save(img_file, 'PNG')
        img_file.close()

        image = Image.open(img)
        photo = ImageTk.PhotoImage(image)
        self.img_label.configure(image=photo)
        self.img_label.image = photo


    def save_img(self):
        img_save = tkFileDialog.asksaveasfile(mode='w', defaultextension='.png')
        if img_save:
            self.qrimg.save(img_save)

if __name__ == '__main__':
    root = Tk()
    root.geometry('500x350')
    app = QrCode(root)
    root.mainloop()