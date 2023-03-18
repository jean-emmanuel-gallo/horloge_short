import datetime
import time
import threading
import tkinter as tk

class HorlogeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Horloge")
        self.master.configure(bg="black")
        self.master.geometry("800x600+{}+{}".format(int((self.master.winfo_screenwidth() - 800) / 2), int((self.master.winfo_screenheight() - 600) / 2)))
        
        self.heure_var = tk.StringVar()
        self.heure_label = tk.Label(self.master, textvariable=self.heure_var, font=("Impact", 72), fg="white", bg="black")
        self.heure_label.pack()
        
        self.alarme_var = tk.StringVar()
        self.alarme_entry = tk.Entry(self.master, textvariable=self.alarme_var, font=("Arial", 24), justify="center")
        self.alarme_entry.pack()
        
        self.alarme_btn = tk.Button(self.master, text="Régler l'alarme", font=("Arial", 24), command=self.regler_alarme)
        self.alarme_btn.pack()
        
        self.alarme_thread = threading.Thread(target=self.verifier_alarme)
        self.alarme_thread.start()
        
        self.actualiser_heure()
        
    def actualiser_heure(self):
        now = datetime.datetime.now()
        self.heure_var.set(now.strftime("%H:%M:%S"))
        self.master.after(1000, self.actualiser_heure)
        
    def regler_alarme(self):
        try:
            alarme = datetime.datetime.strptime(self.alarme_var.get(), "%H:%M:%S").time()
            self.alarme_var.set("")
            self.alarme_label = tk.Label(self.master, text="Alarme réglée à {}:{}:{}".format(alarme.hour, alarme.minute, alarme.second), font=("Arial", 24), fg="white", bg="black")
            self.alarme_label.pack()
        except ValueError:
            pass
    
    def verifier_alarme(self):
        while True:
            now = datetime.datetime.now().time()
            if hasattr(self, "alarme_label"):
                alarme = datetime.datetime.strptime(self.alarme_label.cget("text").split()[3], "%H:%M:%S").time()
                if now.hour == alarme.hour and now.minute == alarme.minute and now.second == alarme.second:
                    self.alarme_sonner()
            time.sleep(1)
            
    def alarme_sonner(self):
        self.alarme_label.config(text="L'alarme sonne !", font=("Arial", 24, "bold"), fg="red")
        self.master.bell()
        time.sleep(2)
        self.alarme_label.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = HorlogeGUI(root)
    root.mainloop()
