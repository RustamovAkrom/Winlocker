import tkinter as tk
import hashlib

# Firstly password should be set in .env file as PASSWORD=your_password
PASSWORD_HASH = hashlib.sha256("2007".encode()).hexdigest()
# PASSWORD_HASH = "f1cfa5ebb149e8099d561aae57beed6c68f990f45a910ea9d7b460dbcc5350be"
# Maximum allowed attempts before lockout
MAX_ATTEMPTS = 3
LOCK_TIME = 10  # seconds

class WinLock:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.attempts = 0
        self.locked = False
        self.remaining = 0

        self.setup_window()
        self.build_ui()

    def setup_window(self):
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.protocol("WM_DELETE_WINDOW", lambda: None) # Block close
        self.root.bind("<FocusOut>", lambda e: self.root.focus_force()) # Keep focus

    def build_ui(self):
        self.container = tk.Frame(self.root, bg="black")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.container,
            text="COMPUTER LOCKED",
            fg="white",
            bg="black",
            font=("Segoe UI", 36, "bold")
        ).pack(pady=20)

        tk.Label(
            self.container,
            text="Enter password to unlock",
            fg="gray",
            bg="black",
            font=("Segoe UI", 16)
        ).pack(pady=10)

        self.entry = tk.Entry(
            self.container,
            font=("Segoe UI", 24),
            show="*",
            justify="center",
            width=20
        )
        self.entry.pack(pady=20)
        self.entry.focus()
        self.entry.bind("<Return>", self.check_password)

        self.status = tk.Label(
            self.container,
            text="",
            fg="red",
            bg="black",
            font=("Segoe UI", 14)
        )
        self.status.pack()

    def check_password(self, event=None):
        if self.locked:
            return

        pwd = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        if not pwd:
            self.status.config(text="Please enter a password", fg="red")
            return

        # Check password
        hashed = hashlib.sha256(pwd.encode()).hexdigest()

        if hashed == PASSWORD_HASH:
            self.root.destroy()
        else:
            self.attempts += 1
            self.status.config(text="Wrong password", fg="red")

            if self.attempts >= MAX_ATTEMPTS:
                self.start_lock()
    def start_lock(self):
        self.locked = True
        self.remaining = LOCK_TIME
        self.attempts = 0
        self.update_timer()

    def update_timer(self):
        if self.remaining <= 0:
            self.locked = False
            self.status.config(text="", fg="red")
            return
        
        self.status.config(text=f"Locked. Wait {self.remaining} sec", fg="red")
        self.remaining -= 1
        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = WinLock(root)
    root.mainloop()
