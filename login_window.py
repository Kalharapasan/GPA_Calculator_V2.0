import tkinter as tk
from tkinter import messagebox, ttk
from database_manager import DatabaseManager
import re

class LoginWindow:
    """Modern login and registration window with improved UI"""
    
    def __init__(self, parent, db_manager: DatabaseManager, callback):
        self.parent = parent
        self.db_manager = db_manager
        self.callback = callback
        
        # Create login window
        self.login_window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.center_window()
    
    def setup_window(self):
        """Configure the login window"""
        self.login_window.title("GPA Calculator - Login")
        self.login_window.geometry("400x550")
        self.login_window.config(bg="#f8f9fa")
        self.login_window.grab_set()  # Modal window
        self.login_window.resizable(False, False)
        
        try:
            self.login_window.iconbitmap('icon.ico')  # Optional icon
        except:
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (550 // 2)
        self.login_window.geometry(f"400x550+{x}+{y}")
    
    def create_widgets(self):
        """Create and layout all widgets"""
        main_frame = tk.Frame(self.login_window, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.create_header(main_frame)
        self.create_login_section(main_frame)
        self.create_divider(main_frame)
        self.create_register_section(main_frame)
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="#f8f9fa")
        header_frame.pack(fill="x", pady=(0, 30))
        
        logo_frame = tk.Frame(header_frame, width=60, height=60, bg="#007bff")
        logo_frame.pack()
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text="📊", font=("Arial", 24), bg="#007bff", fg="white")
        logo_label.pack(expand=True)
        
        title_label = tk.Label(header_frame, text="GPA Calculator", font=("Segoe UI", 20, "bold"), bg="#f8f9fa", fg="#212529")
        title_label.pack(pady=(10, 0))
        
        subtitle_label = tk.Label(header_frame, text="Track your academic progress", font=("Segoe UI", 10), bg="#f8f9fa", fg="#6c757d")
        subtitle_label.pack()
    
    def create_login_section(self, parent):
        login_frame = tk.LabelFrame(parent, text="Sign In", font=("Segoe UI", 12, "bold"), bg="#f8f9fa", fg="#495057", bd=1, relief="solid")
        login_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(login_frame, text="Username", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20, pady=(15, 5))
        self.login_username = tk.Entry(login_frame, font=("Segoe UI", 11), width=30, relief="solid", bd=1)
        self.login_username.pack(padx=20, pady=(0, 10), ipady=8)
        
        tk.Label(login_frame, text="Password", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20, pady=(0, 5))
        self.login_password = tk.Entry(login_frame, font=("Segoe UI", 11), width=30, show="*", relief="solid", bd=1)
        self.login_password.pack(padx=20, pady=(0, 15), ipady=8)
        
        login_btn = tk.Button(login_frame, text="Sign In", command=self.login, font=("Segoe UI", 11, "bold"), bg="#007bff", fg="white", relief="flat", width=25, pady=10, cursor="hand2")
        login_btn.pack(padx=20, pady=(0, 20))
        
        self.login_password.bind("<Return>", lambda e: self.login())
    
    def create_divider(self, parent):
        divider_frame = tk.Frame(parent, height=1, bg="#dee2e6")
        divider_frame.pack(fill="x", pady=15)
        
        or_label = tk.Label(parent, text="OR", font=("Segoe UI", 10), bg="#f8f9fa", fg="#6c757d")
        or_label.pack()
    
    def create_register_section(self, parent):
        register_frame = tk.LabelFrame(parent, text="Create New Account", font=("Segoe UI", 12, "bold"), bg="#f8f9fa", fg="#495057", bd=1, relief="solid")
        register_frame.pack(fill="x", pady=(15, 0))
        
        tk.Label(register_frame, text="Username", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20, pady=(15, 5))
        self.register_username = tk.Entry(register_frame, font=("Segoe UI", 11), width=30, relief="solid", bd=1)
        self.register_username.pack(padx=20, pady=(0, 10), ipady=8)
        
        tk.Label(register_frame, text="Email (optional)", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20, pady=(0, 5))
        self.register_email = tk.Entry(register_frame, font=("Segoe UI", 11), width=30, relief="solid", bd=1)
        self.register_email.pack(padx=20, pady=(0, 10), ipady=8)
        
        tk.Label(register_frame, text="Password", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20, pady=(0, 5))
        self.register_password = tk.Entry(register_frame, font=("Segoe UI", 11), width=30, show="*", relief="solid", bd=1)
        self.register_password.pack(padx=20, pady=(0, 10), ipady=8)
        
        tk.Label(register_frame, text="Confirm Password", font=("Segoe UI", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20, pady=(0, 5))
        self.confirm_password = tk.Entry(register_frame, font=("Segoe UI", 11), width=30, show="*", relief="solid", bd=1)
        self.confirm_password.pack(padx=20, pady=(0, 15), ipady=8)
        
        register_btn = tk.Button(register_frame, text="Create Account", command=self.register, font=("Segoe UI", 11, "bold"), bg="#28a745", fg="white", relief="flat", width=25, pady=10, cursor="hand2")
        register_btn.pack(padx=20, pady=(0, 20))
    
    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="#f8f9fa")
        footer_frame.pack(fill="x", pady=(20, 0))
        footer_label = tk.Label(footer_frame, text="Secure login • Your data is encrypted", font=("Segoe UI", 9), bg="#f8f9fa", fg="#6c757d")
        footer_label.pack()
    
    def validate_email(self, email: str) -> bool:
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.", parent=self.login_window)
            return
        
        try:
            user_id = self.db_manager.authenticate_user(username, password)
            if user_id:
                self.login_window.destroy()
                self.callback(user_id, username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.", parent=self.login_window)
                self.login_password.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}", parent=self.login_window)
    
    def register(self):
        username = self.register_username.get().strip()
        email = self.register_email.get().strip()
        password = self.register_password.get()
        confirm_password = self.confirm_password.get()

        if not username or not password:
            messagebox.showerror("Registration Error", "Username and password are required.", parent=self.login_window)
            return

        if len(username) < 3:
            messagebox.showerror("Registration Error", "Username must be at least 3 characters long.", parent=self.login_window)
            return

        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters long.", parent=self.login_window)
            return

        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match.", parent=self.login_window)
            return

        if email and not self.validate_email(email):
            messagebox.showerror("Registration Error", "Please enter a valid email address.", parent=self.login_window)
            return

        try:
            user_id = self.db_manager.register_user(username, password, email)
            if user_id:
                messagebox.showinfo("Success", "Account created successfully!", parent=self.login_window)

                # ✅ Auto-login after registration
                self.login_window.destroy()
                self.callback(user_id, username)
            else:
                messagebox.showerror("Registration Error", "Username already exists. Please choose a different username.", parent=self.login_window)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}", parent=self.login_window)
