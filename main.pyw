import tkinter as tk
from tkinter.filedialog import askopenfilename


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

    def uploadFile(self):
        file_path = askopenfilename(filetypes=[(
            'Excel files', '*.xlsx')], title="Subir archivo")
        if file_path:
            fileName = file_path.split('/')[-1]
            self.fileName.config(text=fileName)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
