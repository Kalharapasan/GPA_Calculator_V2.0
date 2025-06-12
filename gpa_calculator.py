import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from database_manager import DatabaseManager
from login_window import LoginWindow
import json
from datetime import datetime
from typing import List, Dict, Optional

# Grade to GPA mapping with more comprehensive options
GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0, "W": 0.0, "I": 0.0
}

class ModernGPACalculator:
    """Modern GPA Calculator with enhanced UI and features"""
    
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        
        # Application state
        self.dark_mode = False
        self.entries = []
        self.db_manager = DatabaseManager()
        self.current_user_id = None
        self.current_username = None
        
        # Theme colors
        self.light_theme = {
            'bg': '#f8f9fa',
            'fg': '#212529',
            'accent': '#007bff',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'secondary': '#6c757d',
            'card_bg': '#ffffff',
            'border': '#dee2e6'
        }
        
        self.dark_theme = {
            'bg': '#212529',
            'fg': '#f8f9fa',
            'accent': '#0d6efd',
            'success': '#198754',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'secondary': '#adb5bd',
            'card_bg': '#343a40',
            'border': '#495057'
        }
        
        self.current_theme = self.light_theme
        
        # Show login window first
        self.show_login()
    
    def setup_main_window(self):
        """Configure the main application window"""
        self.root.title("Advanced GPA Calculator")
        self.root.geometry("900x700")
        self.root.config(bg="#f8f9fa")
        self.root.minsize(800, 600)
        
        # Center window
        self.center_window()
        
        # Configure grid weights for responsive design
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
    
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
    
    def show_login(self):
        """Show login window"""
        LoginWindow(self.root, self.db_manager, self.on_login_success)
    
    def on_login_success(self, user_id: int, username: str):
        """Called when user successfully logs in"""
        self.current_user_id = user_id
        self.current_username = username
        self.create_main_interface()
        self.load_data()
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create sections
        self.create_header()
        self.create_toolbar()
        self.create_course_table()
        self.create_results_section()
        self.create_status_bar()
    
    def create_header(self):
        """Create application header with user info"""
        header_frame = tk.Frame(self.main_frame, bg=self.current_theme['bg'])
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Left side - Welcome message
        welcome_frame = tk.Frame(header_frame, bg=self.current_theme['bg'])
        welcome_frame.pack(side="left")
        
        welcome_label = tk.Label(welcome_frame, 
                                text=f"Welcome back, {self.current_username}!", 
                                font=("Segoe UI", 16, "bold"), 
                                bg=self.current_theme['bg'], 
                                fg=self.current_theme['fg'])
        welcome_label.pack(anchor="w")
        
        date_label = tk.Label(welcome_frame, 
                             text=datetime.now().strftime("%B %d, %Y"), 
                             font=("Segoe UI", 10), 
                             bg=self.current_theme['bg'], 
                             fg=self.current_theme['secondary'])
        date_label.pack(anchor="w")
        
        # Right side - User actions
        actions_frame = tk.Frame(header_frame, bg=self.current_theme['bg'])
        actions_frame.pack(side="right")
        
        # Theme toggle
        theme_btn = tk.Button(actions_frame, text="🌓", 
                             command=self.toggle_theme, 
                             font=("Segoe UI", 12),
                             bg=self.current_theme['card_bg'], 
                             fg=self.current_theme['fg'],
                             relief="flat", bd=1, padx=10,
                             cursor="hand2")
        theme_btn.pack(side="right", padx=(10, 0))
        
        # Logout button
        logout_btn = tk.Button(actions_frame, text="Logout", 
                              command=self.logout, 
                              font=("Segoe UI", 10),
                              bg=self.current_theme['danger'], 
                              fg="white",
                              relief="flat", padx=15, cursor="hand2")
        logout_btn.pack(side="right")
    
    def create_toolbar(self):
        """Create toolbar with action buttons"""
        toolbar_frame = tk.Frame(self.main_frame, bg=self.current_theme['card_bg'], 
                                relief="solid", bd=1)
        toolbar_frame.pack(fill="x", pady=(0, 15))
        
        # Left side buttons
        left_buttons = tk.Frame(toolbar_frame, bg=self.current_theme['card_bg'])
        left_buttons.pack(side="left", padx=15, pady=10)
        
        # Add course button
        add_btn = tk.Button(left_buttons, text="+ Add Course", 
                           command=self.add_course_row,
                           font=("Segoe UI", 10, "bold"),
                           bg=self.current_theme['accent'], fg="white",
                           relief="flat", padx=20, pady=8, cursor="hand2")
        add_btn.pack(side="left", padx=(0, 10))
        
        # Import/Export buttons
        import_btn = tk.Button(left_buttons, text="📁 Import", 
                              command=self.import_data,
                              font=("Segoe UI", 10),
                              bg=self.current_theme['secondary'], fg="white",
                              relief="flat", padx=15, pady=8, cursor="hand2")
        import_btn.pack(side="left", padx=(0, 5))
        
        export_btn = tk.Button(left_buttons, text="💾 Export", 
                              command=self.export_data,
                              font=("Segoe UI", 10),
                              bg=self.current_theme['secondary'], fg="white",
                              relief="flat", padx=15, pady=8, cursor="hand2")
        export_btn.pack(side="left", padx=(0, 10))
        
        # Right side buttons
        right_buttons = tk.Frame(toolbar_frame, bg=self.current_theme['card_bg'])
        right_buttons.pack(side="right", padx=15, pady=10)
        
        # Clear all button
        clear_btn = tk.Button(right_buttons, text="🗑️ Clear All", 
                             command=self.clear_all_courses,
                             font=("Segoe UI", 10),
                             bg=self.current_theme['danger'], fg="white",
                             relief="flat", padx=15, pady=8, cursor="hand2")
        clear_btn.pack(side="right", padx=(10, 0))
        
        # Save button
        save_btn = tk.Button(right_buttons, text="💾 Save", 
                            command=self.save_data,
                            font=("Segoe UI", 10, "bold"),
                            bg=self.current_theme['success'], fg="white",
                            relief="flat", padx=20, pady=8, cursor="hand2")
        save_btn.pack(side="right")
    
    def create_course_table(self):
        """Create course input table with modern styling"""
        # Table container
        table_container = tk.Frame(self.main_frame, bg=self.current_theme['card_bg'], 
                                  relief="solid", bd=1)
        table_container.pack(fill="both", expand=True, pady=(0, 15))
        
        # Table header
        header_frame = tk.Frame(table_container, bg=self.current_theme['accent'], height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Header labels
        headers = ["Course Name", "Course Code", "Grade", "Credits", "Semester", "Year", "Action"]
        weights = [3, 2, 1, 1, 2, 1, 1]
        
        for i, (header, weight) in enumerate(zip(headers, weights)):
            label = tk.Label(header_frame, text=header, 
                           font=("Segoe UI", 11, "bold"),
                           bg=self.current_theme['accent'], fg="white")
            label.grid(row=0, column=i, sticky="ew", padx=5, pady=15)
            header_frame.grid_columnconfigure(i, weight=weight)
        
        # Scrollable content area
        canvas_frame = tk.Frame(table_container, bg=self.current_theme['card_bg'])
        canvas_frame.pack(fill="both", expand=True)
        
        # Canvas and scrollbar
        self.canvas = tk.Canvas(canvas_frame, bg=self.current_theme['card_bg'], 
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.current_theme['card_bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure scrollable frame columns
        for i, weight in enumerate(weights):
            self.scrollable_frame.grid_columnconfigure(i, weight=weight)
    
    def create_results_section(self):
        """Create results display section"""
        results_frame = tk.Frame(self.main_frame, bg=self.current_theme['card_bg'], 
                                relief="solid", bd=1)
        results_frame.pack(fill="x", pady=(0, 15))
        
        # Results header
        results_header = tk.Frame(results_frame, bg=self.current_theme['accent'], height=40)
        results_header.pack(fill="x")
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📊 Academic Summary", 
                font=("Segoe UI", 12, "bold"),
                bg=self.current_theme['accent'], fg="white").pack(pady=10)
        
        # Results content
        results_content = tk.Frame(results_frame, bg=self.current_theme['card_bg'])
        results_content.pack(fill="x", padx=20, pady=20)
        
        # GPA Display (large and prominent)
        gpa_frame = tk.Frame(results_content, bg=self.current_theme['card_bg'])
        gpa_frame.pack(side="left", padx=(0, 40))
        
        tk.Label(gpa_frame, text="Current GPA", 
                font=("Segoe UI", 12),
                bg=self.current_theme['card_bg'], 
                fg=self.current_theme['secondary']).pack()
        
        self.gpa_display = tk.Label(gpa_frame, text="0.00", 
                                   font=("Segoe UI", 32, "bold"),
                                   bg=self.current_theme['card_bg'], 
                                   fg=self.current_theme['accent'])
        self.gpa_display.pack()
        
        # Statistics
        stats_frame = tk.Frame(results_content, bg=self.current_theme['card_bg'])
        stats_frame.pack(side="left", fill="x", expand=True)
        
        # Stats grid
        stats_grid = tk.Frame(stats_frame, bg=self.current_theme['card_bg'])
        stats_grid.pack(fill="x")
        
        # Total Credits
        credits_frame = tk.Frame(stats_grid, bg=self.current_theme['card_bg'])
        credits_frame.grid(row=0, column=0, sticky="w", padx=(0, 30))
        
        tk.Label(credits_frame, text="Total Credits", 
                font=("Segoe UI", 10),
                bg=self.current_theme['card_bg'], 
                fg=self.current_theme['secondary']).pack()
        
        self.credits_display = tk.Label(credits_frame, text="0", 
                                       font=("Segoe UI", 18, "bold"),
                                       bg=self.current_theme['card_bg'], 
                                       fg=self.current_theme['fg'])
        self.credits_display.pack()
        
        # Total Courses
        courses_frame = tk.Frame(stats_grid, bg=self.current_theme['card_bg'])
        courses_frame.grid(row=0, column=1, sticky="w", padx=(0, 30))
        
        tk.Label(courses_frame, text="Total Courses", 
                font=("Segoe UI", 10),
                bg=self.current_theme['card_bg'], 
                fg=self.current_theme['secondary']).pack()
        
        self.courses_display = tk.Label(courses_frame, text="0", 
                                       font=("Segoe UI", 18, "bold"),
                                       bg=self.current_theme['card_bg'], 
                                       fg=self.current_theme['fg'])
        self.courses_display.pack()
        
        # GPA Status
        status_frame = tk.Frame(stats_grid, bg=self.current_theme['card_bg'])
        status_frame.grid(row=0, column=2, sticky="w")
        
        tk.Label(status_frame, text="Status", 
                font=("Segoe UI", 10),
                bg=self.current_theme['card_bg'], 
                fg=self.current_theme['secondary']).pack()
        
        self.status_display = tk.Label(status_frame, text="--", 
                                      font=("Segoe UI", 12, "bold"),
                                      bg=self.current_theme['card_bg'], 
                                      fg=self.current_theme['secondary'])
        self.status_display.pack()
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Frame(self.main_frame, bg=self.current_theme['border'], 
                                  height=30)
        self.status_bar.pack(fill="x")
        self.status_bar.pack_propagate(False)
        
        self.status_text = tk.Label(self.status_bar, text="Ready", 
                                   font=("Segoe UI", 9),
                                   bg=self.current_theme['border'], 
                                   fg=self.current_theme['secondary'])
        self.status_text.pack(side="left", padx=10, pady=5)
        
        # Auto-save indicator
        self.autosave_indicator = tk.Label(self.status_bar, text="●", 
                                          font=("Segoe UI", 12),
                                          bg=self.current_theme['border'], 
                                          fg=self.current_theme['success'])
        self.autosave_indicator.pack(side="right", padx=10, pady=5)
    
    def add_course_row(self, course="", code="", grade="A", credits="", 
                      semester="", year=""):
        """Add a new course row to the table"""
        row = len(self.entries)
        
        # Course name
        course_entry = tk.Entry(self.scrollable_frame, font=("Segoe UI", 10), 
                               relief="solid", bd=1)
        course_entry.grid(row=row, column=0, sticky="ew", padx=5, pady=5, ipady=8)
        course_entry.insert(0, course)
        
        # Course code
        code_entry = tk.Entry(self.scrollable_frame, font=("Segoe UI", 10), 
                             relief="solid", bd=1)
        code_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5, ipady=8)
        code_entry.insert(0, code)
        
        # Grade dropdown
        grade_var = tk.StringVar(value=grade)
        grade_combo = ttk.Combobox(self.scrollable_frame, textvariable=grade_var, 
                                  values=list(GRADE_POINTS.keys()), 
                                  font=("Segoe UI", 10), width=6, state="readonly")
        grade_combo.grid(row=row, column=2, sticky="ew", padx=5, pady=5, ipady=8)
        
        # Credits
        credits_entry = tk.Entry(self.scrollable_frame, font=("Segoe UI", 10), 
                                relief="solid", bd=1)
        credits_entry.grid(row=row, column=3, sticky="ew", padx=5, pady=5, ipady=8)
        credits_entry.insert(0, credits)
        
        # Semester
        semester_entry = tk.Entry(self.scrollable_frame, font=("Segoe UI", 10), 
                                 relief="solid", bd=1)
        semester_entry.grid(row=row, column=4, sticky="ew", padx=5, pady=5, ipady=8)
        semester_entry.insert(0, semester)
        
        # Year
        year_entry = tk.Entry(self.scrollable_frame, font=("Segoe UI", 10), 
                             relief="solid", bd=1)
        year_entry.grid(row=row, column=5, sticky="ew", padx=5, pady=5, ipady=8)
        year_entry.insert(0, year)
        
        # Delete button
        delete_btn = tk.Button(self.scrollable_frame, text="🗑️", 
                              command=lambda r=row: self.remove_course_row(r),
                              font=("Segoe UI", 10),
                              bg=self.current_theme['danger'], fg="white",
                              relief="flat", width=3, cursor="hand2")
        delete_btn.grid(row=row, column=6, padx=5, pady=5, ipady=5)
        
        # Store entry references
        entry_data = {
            'course': course_entry,
            'code': code_entry,
            'grade': grade_var,
            'credits': credits_entry,
            'semester': semester_entry,
            'year': year_entry,
            'delete_btn': delete_btn
        }
        
        self.entries.append(entry_data)
        
        # Bind events for real-time calculation
        grade_var.trace("w", lambda *args: self.calculate_gpa())
        credits_entry.bind("<KeyRelease>", lambda e: self.calculate_gpa())
        course_entry.bind("<KeyRelease>", lambda e: self.auto_save())
        
        # Update canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def remove_course_row(self, index):
        """Remove a course row"""
        if len(self.entries) <= 1:
            messagebox.showwarning("Warning", 
                                 "You must have at least one course row.",
                                 parent=self.root)
            return
        
        # Destroy widgets
        entry = self.entries[index]
        for widget in entry.values():
            if hasattr(widget, 'destroy'):
                widget.destroy()
        
        # Remove from list
        self.entries.pop(index)
        
        # Reindex remaining entries
        self.reindex_entries()
        self.calculate_gpa()
        
        # Update status
        self.update_status("Course removed")
    
    def reindex_entries(self):
        """Reindex delete button commands after removal"""
        for i, entry in enumerate(self.entries):
            entry['delete_btn'].config(command=lambda r=i: self.remove_course_row(r))
    
    def calculate_gpa(self):
        """Calculate and display GPA with enhanced statistics"""
        total_credits = 0
        total_points = 0
        valid_courses = 0
        grade_distribution = {}
        
        for entry in self.entries:
            try:
                grade = entry['grade'].get()
                credits_text = entry['credits'].get().strip()
                
                if not credits_text:
                    continue
                    
                credits = float(credits_text)
                
                if credits > 0 and entry['course'].get().strip():
                    total_credits += credits
                    points = GRADE_POINTS.get(grade, 0) * credits
                    total_points += points
                    valid_courses += 1
                    
                    # Track grade distribution
                    grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
                    
            except ValueError:
                continue
        
        # Calculate GPA
        gpa = total_points / total_credits if total_credits > 0 else 0.0
        
        # Update displays
        self.gpa_display.config(text=f"{gpa:.2f}")
        self.credits_display.config(text=f"{total_credits:.1f}")
        self.courses_display.config(text=str(valid_courses))
        
        # Update GPA status with color coding
        if gpa >= 3.7:
            status = "Excellent"
            color = self.current_theme['success']
        elif gpa >= 3.3:
            status = "Good"
            color = self.current_theme['accent']
        elif gpa >= 3.0:
            status = "Satisfactory"
            color = self.current_theme['warning']
        elif gpa >= 2.0:
            status = "Needs Improvement"
            color = self.current_theme['danger']
        else:
            status = "Critical"
            color = self.current_theme['danger']
        
        self.status_display.config(text=status, fg=color)
        
        # Update GPA display color
        if gpa >= 3.5:
            self.gpa_display.config(fg=self.current_theme['success'])
        elif gpa >= 3.0:
            self.gpa_display.config(fg=self.current_theme['accent'])
        elif gpa >= 2.5:
            self.gpa_display.config(fg=self.current_theme['warning'])
        else:
            self.gpa_display.config(fg=self.current_theme['danger'])
    
    def save_data(self):
        """Save course data to database"""
        if not self.current_user_id:
            messagebox.showerror("Error", "No user logged in.", parent=self.root)
            return
        
        courses_data = []
        for entry in self.entries:
            course = entry['course'].get().strip()
            code = entry['code'].get().strip()
            grade = entry['grade'].get()
            credits = entry['credits'].get().strip()
            semester = entry['semester'].get().strip()
            year = entry['year'].get().strip()
            
            if course and credits:
                try:
                    float(credits)  # Validate credits
                    courses_data.append({
                        "course": course,
                        "code": code,
                        "grade": grade,
                        "credits": credits,
                        "semester": semester,
                        "year": year
                    })
                except ValueError:
                    continue
        
        if not courses_data:
            messagebox.showwarning("Warning", "No valid courses to save.", 
                                 parent=self.root)
            return
        
        try:
            self.db_manager.save_courses(self.current_user_id, courses_data)
            self.update_status(f"Saved {len(courses_data)} courses successfully!")
            
            # Update autosave indicator
            self.autosave_indicator.config(fg=self.current_theme['success'])
            self.root.after(2000, lambda: self.autosave_indicator.config(
                fg=self.current_theme['secondary']))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}", 
                               parent=self.root)
    
    def load_data(self):
        """Load course data from database"""
        if not self.current_user_id:
            return
        
        try:
            courses_data = self.db_manager.load_courses(self.current_user_id)
            
            # Clear existing entries
            self.clear_entries()
            
            # Load data or add empty row
            if courses_data:
                for course_data in courses_data:
                    self.add_course_row(
                        course=course_data.get("course", ""),
                        code=course_data.get("code", ""),
                        grade=course_data.get("grade", "A"),
                        credits=course_data.get("credits", ""),
                        semester=course_data.get("semester", ""),
                        year=course_data.get("year", "")
                    )
                self.update_status(f"Loaded {len(courses_data)} courses")
            else:
                self.add_course_row()  # Add empty row if no data
                self.update_status("No saved courses found")
            
            self.calculate_gpa()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}", 
                               parent=self.root)
            self.add_course_row()
    
    def clear_entries(self):
        """Clear all entry widgets"""
        for entry in self.entries:
            for widget in entry.values():
                if hasattr(widget, 'destroy'):
                    widget.destroy()
        self.entries.clear()
    
    def clear_all_courses(self):
        """Clear all course entries with confirmation"""
        if messagebox.askyesno("Confirm Clear", 
                              "Are you sure you want to clear all courses?\n"
                              "This action cannot be undone.", 
                              parent=self.root):
            self.clear_entries()
            self.add_course_row()
            self.calculate_gpa()
            self.update_status("All courses cleared")
    
    def auto_save(self):
        """Auto-save functionality (triggered on data change)"""
        # Implement auto-save with debouncing
        if hasattr(self, 'auto_save_timer'):
            self.root.after_cancel(self.auto_save_timer)
        
        self.auto_save_timer = self.root.after(3000, self._perform_auto_save)
    
    def _perform_auto_save(self):
        """Perform the actual auto-save operation"""
        if self.current_user_id:
            try:
                # Get current data
                courses_data = []
                for entry in self.entries:
                    course = entry['course'].get().strip()
                    if course and entry['credits'].get().strip():
                        try:
                            float(entry['credits'].get())
                            courses_data.append({
                                "course": course,
                                "code": entry['code'].get().strip(),
                                "grade": entry['grade'].get(),
                                "credits": entry['credits'].get().strip(),
                                "semester": entry['semester'].get().strip(),
                                "year": entry['year'].get().strip()
                            })
                        except ValueError:
                            continue
                
                if courses_data:
                    self.db_manager.save_courses(self.current_user_id, courses_data)
                    self.autosave_indicator.config(fg=self.current_theme['success'])
                    self.root.after(1000, lambda: self.autosave_indicator.config(
                        fg=self.current_theme['secondary']))
                
            except Exception:
                pass  # Silently fail auto-save
    
    def export_data(self):
        """Export data to JSON file"""
        if not self.entries:
            messagebox.showwarning("Warning", "No data to export.", parent=self.root)
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export GPA Data"
            )
            
            if filename:
                # Prepare export data
                export_data = {
                    "user": self.current_username,
                    "export_date": datetime.now().isoformat(),
                    "courses": []
                }
                
                for entry in self.entries:
                    course = entry['course'].get().strip()
                    if course:
                        export_data["courses"].append({
                            "course": course,
                            "code": entry['code'].get().strip(),
                            "grade": entry['grade'].get(),
                            "credits": entry['credits'].get().strip(),
                            "semester": entry['semester'].get().strip(),
                            "year": entry['year'].get().strip()
                        })
                
                # Write to file
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                self.update_status(f"Data exported to {filename}")
                messagebox.showinfo("Success", "Data exported successfully!", 
                                  parent=self.root)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}", 
                               parent=self.root)
    
    def import_data(self):
        """Import data from JSON file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Import GPA Data"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
                
                if "courses" not in import_data:
                    messagebox.showerror("Error", "Invalid file format.", 
                                       parent=self.root)
                    return
                
                # Confirm import
                course_count = len(import_data["courses"])
                if messagebox.askyesno("Confirm Import", 
                                     f"Import {course_count} courses?\n"
                                     "This will replace your current data.",
                                     parent=self.root):
                    
                    # Clear existing data
                    self.clear_entries()
                    
                    # Import courses
                    for course_data in import_data["courses"]:
                        self.add_course_row(
                            course=course_data.get("course", ""),
                            code=course_data.get("code", ""),
                            grade=course_data.get("grade", "A"),
                            credits=course_data.get("credits", ""),
                            semester=course_data.get("semester", ""),
                            year=course_data.get("year", "")
                        )
                    
                    if not self.entries:
                        self.add_course_row()
                    
                    self.calculate_gpa()
                    self.update_status(f"Imported {course_count} courses")
                    messagebox.showinfo("Success", "Data imported successfully!", 
                                      parent=self.root)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}", 
                               parent=self.root)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        self.current_theme = self.dark_theme if self.dark_mode else self.light_theme
        
        # Update main window
        self.root.config(bg=self.current_theme['bg'])
        
        # Recreate interface with new theme
        self.main_frame.destroy()
        self.create_main_interface()
        self.load_data()
        
        theme_name = "Dark" if self.dark_mode else "Light"
        self.update_status(f"Switched to {theme_name} theme")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_text.config(text=message)
        # Clear message after 5 seconds
        self.root.after(5000, lambda: self.status_text.config(text="Ready"))
    
    def logout(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", 
                              "Are you sure you want to logout?\n"
                              "Make sure to save your changes.", 
                              parent=self.root):
            # Clear user data
            self.current_user_id = None
            self.current_username = None
            
            # Destroy main interface
            if hasattr(self, 'main_frame'):
                self.main_frame.destroy()
            
            # Reset window
            self.root.config(bg="#f8f9fa")
            
            # Show login window
            self.show_login()


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernGPACalculator(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()