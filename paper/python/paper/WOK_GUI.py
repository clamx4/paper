'''
Created on 2015年12月31日

@author: cdz
'''
from paper.webOfKnowledge import *

import tkinter as tk

from os import path
from tkinter import ttk, StringVar

class GUI(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
#         self.database = StringVar(value='ieee')
#         ieee = ttk.Radiobutton(self, text='ieee (25 papers per page)', variable=self.database, value='ieee')
#         ieee.pack()
#         acm_dl = ttk.Radiobutton(self, text='acm_dl (20 papers per page)', variable=self.database, value='acm_dl')
#         acm_dl.pack()
        
        self.label_keyword = tk.Label(self)
        self.label_keyword['text'] = "keyword:"
        self.label_keyword.pack()
        
        self.keyword = tk.Entry(self)
        self.keyword.pack()
        
        self.label_paper_from = tk.Label(self)
        self.label_paper_from['text'] = "paper from(>= 1):"
        self.label_paper_from.pack()
        
        self.paper_from = tk.Entry(self)
        self.paper_from.pack()
        
        self.label_paper_to = tk.Label(self)
        self.label_paper_to['text'] = "paper to(>= 1):"
        self.label_paper_to.pack()
        
        self.paper_to = tk.Entry(self)
        self.paper_to.pack()
        
        self.label_download_path = tk.Label(self)
        self.label_download_path['text'] = '摘要信息存储路径:'
        self.label_download_path.pack()
        
        self.entry_path = tk.Entry(self)
        self.entry_path.pack()
        self.entry_path.insert(0, 'd:\\论文摘要信息.docx')
        
#         self.label_download_interval = tk.Label(self)
#         self.label_download_interval['text'] = 'download interval(seconds):'
#         self.label_download_interval.pack()
#         
#         self.entry_download_interval = tk.Entry(self)
#         self.entry_download_interval.pack()
        
        self.label_warning = tk.Label(self)
        self.label_warning['text'] = ''
        self.label_warning['fg'] = 'red'
        self.label_warning.pack()
        
        self.button_start = tk.Button(self)
        self.button_start["text"] = "start"
        self.button_start["command"] = self.start
        self.button_start.pack(side="top")
        
        

#         self.QUIT = tk.Button(self, text="QUIT", fg="red",
#                               command=root.destroy)
#         self.QUIT.pack(side="bottom")
        
    def start(self):
        keyword = self.keyword.get()
        paper_from = self.paper_from.get()
        paper_to = self.paper_to.get()
        store_path = self.entry_path.get()
#        interval = self.entry_download_interval.get()
#         if not folder_path.endswith('/') and not folder_path.endswith('\\'):
#             if folder_path.find('/') >= 0:
#                 folder_path = ''.join((folder_path, '/'))
#             else:
#                 folder_path = ''.join((folder_path, '\\'))
                
        print(keyword, paper_from, paper_to, store_path)
        if self.check_empty_keyword(keyword) and \
            self.check_paper_from(paper_from) and \
            self.check_paper_to(paper_to):# and \
            #self.check_path(store_path) and \
            #self.check_interval(interval):
            self.warn('正在获取信息')
            #self.download(keyword, int(paper_from), int(paper_to), folder_path, int(interval))
            try:
                start(keyword, int(paper_from), int(paper_to), store_path)
                self.warn('完成')
            except Exception as e:
                print(e)
                self.warn('出错了')
        
    def warn(self, warn_info):
        self.label_warning['text'] = warn_info
        
    def check_empty_keyword(self, keyword):
        if keyword == '':
            self.warn('keyword cannot be empty')
            return False
        return True
    
    def check_paper_from(self, paper_from):
        try:
            x = int(paper_from)
        except Exception:
            self.warn('wrong paper_from number')
            return False
        if x < 1:
            self.warn('paper_from number cannot less than 1')
            return False
        return True
    
    def check_paper_to(self, paper_to):
        try:
            x = int(paper_to)
        except Exception:
            self.warn('wrong paper_to number')
            return False
        if x < 1:
            self.warn('paper_to number cannot less than 1')
            return False
        return True
    
    def check_path(self, folder_path):
        if not path.isdir(folder_path):
            self.warn('wrong store path')
            return False
        return True
    
    def check_interval(self, str_interval):
        try:
            int_interval = int(str_interval)
        except Exception:
            self.warn('wrong delay interval')
            return False
        if int_interval < 1:
            self.warn('delay interval cannot less than 1')
            return False
        return True
    
#    def download(self, keyword, paper_from, paper_to, folder_path, delay):
#         db = self.database.get()
#         downloader = {'ieee' : spide_url,
#                     'acm_dl' : start
#                     }
#         downloader[db](keyword, paper_from, paper_to, folder_path, delay)
        

if __name__ == '__main__':
    DEBUG = 0
    root = tk.Tk()
    root.title('论文摘要信息 - web of knowledge')
    root.geometry('300x365')
    gui = GUI(master = root)
    if DEBUG:
        gui.keyword.insert(0, 'smart home')
        gui.paper_from.insert(0, '132')
        gui.paper_to.insert(0, '132')
        #gui.entry_path.insert(0, 'd:\\p')
        #gui.entry_download_interval.insert(0, '5')
    gui.mainloop()
    pass