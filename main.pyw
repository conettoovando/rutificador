import tkinter as tk
from tkinter.filedialog import askopenfilename
import requests
import pandas as pd
import numpy as np
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rutificador app")
        self.initUI()

    def initUI(self):
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(bg="white")
        self.createWidgets()
        self.route = ''

    def createWidgets(self):
        self.leftFrame = tk.Frame(self, bg="red", width=250, height=600)
        self.leftFrame.pack(side="left", fill="both", expand=True)
        self.rightFrame = tk.Frame(self, bg="blue", width=550, height=600)
        self.rightFrame.pack(side="right", fill="both", expand=True)

        tk.Label(self.leftFrame, text="Subir archivo", bg="red", fg="white",
                 font=("Arial", 16)).pack(side="top", fill="x", pady=10)
        tk.Button(self.leftFrame, text="Subir", bg="red", fg="white",
                  font=("Arial", 16), command=self.uploadFile).pack(side="top", fill="x", pady=10, padx=20)
        tk.Label(self.leftFrame, text="Archivo seleccionado", bg="red", fg="white",
                 font=("Arial", 16))
        tk.Label(self.leftFrame, text="Nombre", bg="red", fg="white",
                 font=("Arial", 16)).pack(side="top", fill="x", pady=10)
        self.fileName = tk.Label(self.leftFrame, text="Ningun archivo seleccionado", bg="red", fg="white",
                                 font=("Arial", 12), justify="center", width=30, wraplength=200)
        self.fileName.pack(side="top", fill="x", pady=10)

        self.box = tk.Frame(self.rightFrame, bg="yellow", width=550, height=30)
        self.box.pack(side="top", fill="both", padx=20, pady=20, ipadx=20, ipady=20, anchor="n")

        self.box2 = tk.Frame(self.rightFrame, bg="green", width=550, height=500)
        self.box2.pack(side="top", fill="both",  padx=20, pady=20, ipadx=20, ipady=20, anchor="n")

        tk.Label(self.box, text="Rut:", bg="yellow", fg="black",
         font=("Arial", 16)).place(x=0, y=20, anchor="w")
        tk.Label(self.box2, text="N° / Rut / Nombre", bg="yellow", fg="black",
         font=("Arial", 16)).place(x=0, y=16, anchor="w")
        
        self.rut = tk.Label(self.box, text="", bg="yellow", fg="black",
         font=("Arial", 16))
        self.rut.place(x=100, y=20, anchor="w")


        self.name = tk.Text(self.box2, bg="yellow", fg="black", font=("Arial", 12), height=22)
        self.name.place(x=0, y=234, anchor="w")


        tk.Button(self.leftFrame, text="Comenzar", bg="cyan", fg="black", width=20,
                  font=("Arial", 16), command=self.start).pack(side="top", fill="x", pady=10, padx=20)

    def uploadFile(self):
        file_path = askopenfilename(filetypes=[(
            'Excel files', '*.xlsx')], title="Subir archivo")
        if file_path:
            self.route = file_path
            fileName = file_path.split('/')[-1]
            self.fileName.config(text=fileName)

    def start(self):
        if self.route:
            column, ColumName = self.openExcel()

            def process_ruts():
                cont = 1
                try:
                    for rut in column:
                        response = self.searchPerson(str(rut))
                        self.rut.config(text=str(rut))
                        if response["data"]["valid"] == False:
                            self.name.insert(tk.END, str(cont+1) + " / " + str(rut) + " / " + str(ColumName[cont-1])+'\n')
                        cont += 1
                except:
                    pass

            t = threading.Thread(target=process_ruts)
            t.start()
        else:
            print("No se ha seleccionado ningún archivo")

    def searchPerson(self, rut):
        url = "https://api.libreapi.cl/rut/validate".format(rut)
        response = requests.get(url, params={"rut": rut})

        response_json = response.json()
        return response_json

    def searchName(self, rut):
        url = "https://api.libreapi.cl/rut/activities".format(rut)
        response = requests.get(url, params={"rut": rut})

        response_json = response.json()
        return response_json

    def openExcel(self):
        df = pd.read_excel(self.route)

        columRut = df['RUT']
        ColumName = df['CLIENTE']
        return columRut, ColumName

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
