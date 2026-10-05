import tkinter as tk
from tkinter import messagebox
import mysql.connector

class BillboardWalkTalk:
    def __init__(self):
        self.roles = {"Designer": False, "Admin": True}
    def process(self, loc, txt):
        return (loc.strip(), txt.strip())
    def to_list(self, rows):
        return[f"ID{r[0]} | 📍 {r[1]} - > \"{r[2]}\"" for r in rows]
        
class DataBaseManagement:
    def __init__(self):
        self.cfg = {
            'host': 'localhost',
            'user':'root',
            'password':
            'LuckySystem',
            'database':'client_billboard'
        }
    def write(self, data):
        try:
            conn = mysql.connector.connect(**self.cfg)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO billboards (location, active_ad_text) VALUES (%s, %s)", data)
            conn.commit()
            conn.close
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", str(err))
            return False

    def read(self):
        try:
            conn = mysql.connector.connect(**self.cfg)
            cursor = conn.cursor()
            cursor.execute("Select id, location, active_ad_text FROM billboards")
            res = cursor.fetchall()
            conn.close()
            return res
        except mysql.connector.Error:
            return[]
                        
class BillboardGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simplified Compact 3-Class System")
        self.geometry("400x450")
                                
        self.model = BillboardWalkTalk()
        self.engine = DataBaseManagement()
        self.role = "Admin"

        tk.Label(self, text="Location:").pack(pady=2)
        self.eloc = tk.Entry(self, width=40)
        self.eloc.pack(pady=2)
 
        tk.Label(self, text="Ad Copy:").pack(pady=2)
        self.etxt = tk.Entry(self, width=40)
        self.etxt.pack(pady=2)

        tk.Button(self, text="Publish to DB", bg="green", fg="white", command=self.submit).pack(pady=5)
        tk.Button(self, text="Refresh Logs", command=self.refresh).pack(pady=2)
                                
        self.box = tk.Listbox(self, width=45, height=10)
        self.box.pack(pady=10)
        self.refresh()

    def submit(self):
      if not self.model.roles.get(self.role):
        return messagebox.showwarning("Denied", "Write access restricted.")
                                    
      if self.eloc.get().strip() and self.etxt.get().strip():
        packet = self.model.process(self.eloc.get(), self.etxt.get())
        if self.engine.write(packet):
            self.eloc.delete(0, tk.END)
            self.etxt.delete(0, tk.END)
            self.refresh()
    def refresh(self):
     self.box.delete(0, tk.END)
     for item in self.model.to_list(self.engine.read()):
      self.box.insert(tk.END, item)


if __name__ == "__main__":
 app = BillboardGUI()
 app.mainloop()
                                                        
                                                        
                                                        
