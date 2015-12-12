'''
Created on 2015年12月7日

@author: cdz
'''

import tkinter as tk

from paper.ACM_DL import start
from os import path
from paper.IEEE import spide_url
from tkinter import ttk, StringVar


class GUI(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.database = StringVar(value='ieee')
        ieee = ttk.Radiobutton(self, text='ieee (25 papers per page)', variable=self.database, value='ieee')
        ieee.pack()
        acm_dl = ttk.Radiobutton(self, text='acm_dl (20 papers per page)', variable=self.database, value='acm_dl')
        acm_dl.pack()
        
        self.label_keyword = tk.Label(self)
        self.label_keyword['text'] = "keyword:"
        self.label_keyword.pack()
        
        self.keyword = tk.Entry(self)
        self.keyword.pack()
        
        self.label_page_from = tk.Label(self)
        self.label_page_from['text'] = "page from(>= 1):"
        self.label_page_from.pack()
        
        self.page_from = tk.Entry(self)
        self.page_from.pack()
        
        self.label_page_to = tk.Label(self)
        self.label_page_to['text'] = "page to(>= 1):"
        self.label_page_to.pack()
        
        self.page_to = tk.Entry(self)
        self.page_to.pack()
        
        self.label_download_path = tk.Label(self)
        self.label_download_path['text'] = 'download folder path:'
        self.label_download_path.pack()
        
        self.entry_path = tk.Entry(self)
        self.entry_path.pack()
        
        self.label_warning = tk.Label(self)
        self.label_warning['text'] = ''
        self.label_warning['fg'] = 'red'
        self.label_warning.pack()
        
        self.button_start = tk.Button(self)
        self.button_start["text"] = "start"
        self.button_start["command"] = self.start
        self.button_start.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.QUIT.pack(side="bottom")
        
    def start(self):
        keyword = self.keyword.get()
        page_from = self.page_from.get()
        page_to = self.page_to.get()
        folder_path = self.entry_path.get()
        if not folder_path.endswith('/') and not folder_path.endswith('\\'):
            if folder_path.find('/') >= 0:
                folder_path = ''.join((folder_path, '/'))
            else:
                folder_path = ''.join((folder_path, '\\'))
                
        print(keyword, page_from, page_to, folder_path)
        if self.check_empty_keyword(keyword) and \
            self.check_page_from(page_from) and \
            self.check_page_to(page_to) and \
            self.check_path(folder_path):
            self.warn('downloading')
            self.download(keyword, int(page_from), int(page_to), folder_path)
            self.warn('complete')
        
    def warn(self, warn_info):
        self.label_warning['text'] = warn_info
        
    def check_empty_keyword(self, keyword):
        if keyword == '':
            self.warn('keyword cannot be empty')
            return False
        return True
    
    def check_page_from(self, page_from):
        try:
            x = int(page_from)
        except Exception:
            self.warn('wrong page_from number')
            return False
        if x < 1:
            self.warn('page_from number cannot less than 1')
            return False
        return True
    
    def check_page_to(self, page_to):
        try:
            x = int(page_to)
        except Exception:
            self.warn('wrong page_to number')
            return False
        if x < 1:
            self.warn('page_to number cannot less than 1')
            return False
        return True
    
    def check_path(self, folder_path):
        if not path.isdir(folder_path):
            self.warn('wrong folder path')
            return False
        return True
    
    def download(self, keyword, page_from, page_to, folder_path):
        db = self.database.get()
        downloader = {'ieee' : spide_url,
                    'acm_dl' : start
                    }
        downloader[db](keyword, page_from, page_to, folder_path)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('paper form IEEE/ACM_DL')
    root.geometry('300x350')
    gui = GUI(master = root)
    gui.mainloop()
    