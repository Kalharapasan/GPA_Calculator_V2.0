import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from datetime import datetime

# Grade to GPA mapping
grade_points = {
    "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.1,
    "D-": 1.0, "F": 0.0
}

class GPACalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Multi-Year GPA Calculator")
        self.root.geometry("800x700")
        self.root.config(bg="#f0f0f0")
        
        self.dark_mode = False
        self.current_year = "Year 1"
        self.current_semester = "Semester 1"
        self.entries = []
        
        # Initialize database
        self.init_database()
        
        self.create_widgets()
        self.load_current_data()

    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT DEFAULT 'default_student',
                year TEXT NOT NULL,
                semester TEXT NOT NULL,
                course_name TEXT NOT NULL,
                grade TEXT NOT NULL,
                credits REAL NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gpa_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT DEFAULT 'default_student',
                year TEXT NOT NULL,
                semester TEXT NOT NULL,
                semester_gpa REAL NOT NULL,
                cumulative_gpa REAL NOT NULL,
                total_credits REAL NOT NULL,
                date_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="Multi-Year GPA Calculator", 
                                   font=("Arial", 18, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        # Year and Semester Selection Frame
        selection_frame = tk.Frame(self.root, bg="#f0f0f0")
        selection_frame.pack(pady=10)
        
        tk.Label(selection_frame, text="Academic Year:", font=("Arial", 12, "bold"), 
                bg="#f0f0f0").grid(row=0, column=0, padx=5)
        
        self.year_var = tk.StringVar(value=self.current_year)
        self.year_combo = ttk.Combobox(selection_frame, textvariable=self.year_var, 
                                      values=["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], 
                                      width=10)
        self.year_combo.grid(row=0, column=1, padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.on_year_semester_change)
        
        tk.Label(selection_frame, text="Semester:", font=("Arial", 12, "bold"), 
                bg="#f0f0f0").grid(row=0, column=2, padx=5)
        
        self.semester_var = tk.StringVar(value=self.current_semester)
        self.semester_combo = ttk.Combobox(selection_frame, textvariable=self.semester_var,
                                          values=["Semester 1", "Semester 2", "Summer"], 
                                          width=12)
        self.semester_combo.grid(row=0, column=3, padx=5)
        self.semester_combo.bind("<<ComboboxSelected>>", self.on_year_semester_change)

        # Table Headers
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(pady=5)
        tk.Label(header_frame, text="Course Name", font=("Arial", 12, "bold"), 
                width=20, bg="#f0f0f0").grid(row=0, column=0, padx=2)
        tk.Label(header_frame, text="Grade", font=("Arial", 12, "bold"), 
                width=8, bg="#f0f0f0").grid(row=0, column=1, padx=2)
        tk.Label(header_frame, text="Credits", font=("Arial", 12, "bold"), 
                width=8, bg="#f0f0f0").grid(row=0, column=2, padx=2)
        tk.Label(header_frame, text="Action", font=("Arial", 12, "bold"), 
                width=8, bg="#f0f0f0").grid(row=0, column=3, padx=2)
        
        # Courses Container with Scrollbar
        canvas_frame = tk.Frame(self.root, bg="#f0f0f0")
        canvas_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", height=200)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.course_frame = self.scrollable_frame

        # Current Semester GPA Display
        gpa_frame = tk.Frame(self.root, bg="#f0f0f0")
        gpa_frame.pack(pady=10)
        
        self.semester_gpa_label = tk.Label(gpa_frame, text="Current Semester GPA: 0.00", 
                                          font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.semester_gpa_label.pack()
        
        self.cumulative_gpa_label = tk.Label(gpa_frame, text="Cumulative GPA: 0.00", 
                                            font=("Arial", 16, "bold"), bg="#f0f0f0", fg="blue")
        self.cumulative_gpa_label.pack()

        # Buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Add Course", command=self.add_course_row, 
                 bg="lightblue", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Save Data", command=self.save_data, 
                 bg="lightgreen", font=("Arial", 10)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="View All Records", command=self.view_all_records, 
                 bg="lightyellow", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Calculate GPA", command=self.calculate_and_save_gpa, 
                 bg="lightcoral", font=("Arial", 10)).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Toggle Dark Mode", command=self.toggle_theme, 
                 bg="gray", font=("Arial", 10)).grid(row=0, column=4, padx=5)

        # Statistics Frame
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(stats_frame, text="Total Credits Completed: 0", 
                                   font=("Arial", 12), bg="#f0f0f0")
        self.stats_label.pack()

    def add_course_row(self, course="", grade="A", credits=""):
        row = len(self.entries)
        
        course_name = tk.Entry(self.course_frame, width=25, font=("Arial", 10))
        course_name.grid(row=row, column=0, padx=2, pady=2)
        course_name.insert(0, course)

        grade_var = tk.StringVar(value=grade)
        grade_dropdown = ttk.Combobox(self.course_frame, textvariable=grade_var, 
                                     values=list(grade_points.keys()), width=8)
        grade_dropdown.grid(row=row, column=1, padx=2, pady=2)

        credits_entry = tk.Entry(self.course_frame, width=8, font=("Arial", 10))
        credits_entry.grid(row=row, column=2, padx=2, pady=2)
        credits_entry.insert(0, credits)

        delete_button = tk.Button(self.course_frame, text="Delete", 
                                 command=lambda: self.remove_course_row(row), 
                                 bg="red", fg="white", font=("Arial", 8))
        delete_button.grid(row=row, column=3, padx=2, pady=2)

        self.entries.append((course_name, grade_var, credits_entry, delete_button))
        
        # Bind events for real-time calculation
        grade_var.trace("w", lambda *args: self.calculate_current_gpa())
        credits_entry.bind("<KeyRelease>", lambda event: self.calculate_current_gpa())
        
        # Update canvas scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def remove_course_row(self, index):
        if index < len(self.entries):
            # Remove widgets
            for widget in self.entries[index]:
                if hasattr(widget, 'destroy'):
                    widget.destroy()
            
            # Remove from list
            self.entries.pop(index)
            
            # Refresh the display
            self.refresh_course_display()
            self.calculate_current_gpa()

    def refresh_course_display(self):
        # Clear all entries
        for entry_set in self.entries:
            for widget in entry_set:
                if hasattr(widget, 'destroy'):
                    widget.destroy()
        
        # Recreate entries
        course_data = []
        for course_name, grade_var, credits_entry, _ in self.entries:
            course_data.append((course_name.get(), grade_var.get(), credits_entry.get()))
        
        self.entries.clear()
        
        for course, grade, credits in course_data:
            self.add_course_row(course, grade, credits)

    def on_year_semester_change(self, event=None):
        self.current_year = self.year_var.get()
        self.current_semester = self.semester_var.get()
        self.load_current_data()

    def calculate_current_gpa(self):
        total_credits = 0
        total_points = 0

        for course_name, grade_var, credits_entry, _ in self.entries:
            grade = grade_var.get()
            try:
                credits = float(credits_entry.get()) if credits_entry.get() else 0
            except ValueError:
                continue

            if credits > 0:
                total_credits += credits
                total_points += grade_points.get(grade, 0) * credits

        if total_credits == 0:
            semester_gpa = 0.00
        else:
            semester_gpa = total_points / total_credits

        self.semester_gpa_label.config(text=f"Current Semester GPA: {semester_gpa:.2f}")
        
        # Calculate cumulative GPA
        self.calculate_cumulative_gpa()
        
        # Update statistics
        total_completed_credits = self.get_total_completed_credits()
        self.stats_label.config(text=f"Total Credits Completed: {total_completed_credits:.1f}")

    def calculate_cumulative_gpa(self):
        # Get all courses from database
        self.cursor.execute('''
            SELECT grade, credits FROM courses 
            WHERE student_id = 'default_student'
        ''')
        
        all_courses = self.cursor.fetchall()
        
        # Add current semester courses if they have valid data
        current_courses = []
        for course_name, grade_var, credits_entry, _ in self.entries:
            course = course_name.get().strip()
            grade = grade_var.get()
            try:
                credits = float(credits_entry.get()) if credits_entry.get() else 0
                if course and credits > 0:
                    current_courses.append((grade, credits))
            except ValueError:
                continue
        
        # Combine all courses
        all_courses.extend(current_courses)
        
        total_credits = 0
        total_points = 0
        
        for grade, credits in all_courses:
            total_credits += credits
            total_points += grade_points.get(grade, 0) * credits
        
        if total_credits == 0:
            cumulative_gpa = 0.00
        else:
            cumulative_gpa = total_points / total_credits
        
        self.cumulative_gpa_label.config(text=f"Cumulative GPA: {cumulative_gpa:.2f}")

    def get_total_completed_credits(self):
        self.cursor.execute('''
            SELECT SUM(credits) FROM courses 
            WHERE student_id = 'default_student'
        ''')
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def save_data(self):
        saved_count = 0
        for course_name, grade_var, credits_entry, _ in self.entries:
            course = course_name.get().strip()
            grade = grade_var.get()
            try:
                credits = float(credits_entry.get()) if credits_entry.get() else 0
            except ValueError:
                continue
            
            if course and credits > 0:
                # Check if course already exists
                self.cursor.execute('''
                    SELECT id FROM courses 
                    WHERE student_id = 'default_student' AND year = ? AND semester = ? AND course_name = ?
                ''', (self.current_year, self.current_semester, course))
                
                existing = self.cursor.fetchone()
                
                if existing:
                    # Update existing course
                    self.cursor.execute('''
                        UPDATE courses 
                        SET grade = ?, credits = ?, date_added = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (grade, credits, existing[0]))
                else:
                    # Insert new course
                    self.cursor.execute('''
                        INSERT INTO courses (student_id, year, semester, course_name, grade, credits)
                        VALUES ('default_student', ?, ?, ?, ?, ?)
                    ''', (self.current_year, self.current_semester, course, grade, credits))
                
                saved_count += 1
        
        self.conn.commit()
        messagebox.showinfo("Saved", f"Saved {saved_count} courses to database.")
        self.calculate_current_gpa()

    def calculate_and_save_gpa(self):
        # First save current data
        self.save_data()
        
        # Calculate current semester GPA
        total_credits = 0
        total_points = 0
        
        self.cursor.execute('''
            SELECT grade, credits FROM courses 
            WHERE student_id = 'default_student' AND year = ? AND semester = ?
        ''', (self.current_year, self.current_semester))
        
        semester_courses = self.cursor.fetchall()
        
        for grade, credits in semester_courses:
            total_credits += credits
            total_points += grade_points.get(grade, 0) * credits
        
        if total_credits > 0:
            semester_gpa = total_points / total_credits
        else:
            semester_gpa = 0.0
        
        # Calculate cumulative GPA
        self.cursor.execute('''
            SELECT grade, credits FROM courses 
            WHERE student_id = 'default_student'
        ''')
        
        all_courses = self.cursor.fetchall()
        
        total_all_credits = 0
        total_all_points = 0
        
        for grade, credits in all_courses:
            total_all_credits += credits
            total_all_points += grade_points.get(grade, 0) * credits
        
        if total_all_credits > 0:
            cumulative_gpa = total_all_points / total_all_credits
        else:
            cumulative_gpa = 0.0
        
        # Save GPA record
        self.cursor.execute('''
            INSERT OR REPLACE INTO gpa_records 
            (student_id, year, semester, semester_gpa, cumulative_gpa, total_credits)
            VALUES ('default_student', ?, ?, ?, ?, ?)
        ''', (self.current_year, self.current_semester, semester_gpa, cumulative_gpa, total_all_credits))
        
        self.conn.commit()
        
        messagebox.showinfo("GPA Calculated", 
                           f"Semester GPA: {semester_gpa:.2f}\n"
                           f"Cumulative GPA: {cumulative_gpa:.2f}\n"
                           f"Total Credits: {total_all_credits:.1f}")

    def load_current_data(self):
        # Clear current entries
        for entry_set in self.entries:
            for widget in entry_set:
                if hasattr(widget, 'destroy'):
                    widget.destroy()
        self.entries.clear()
        
        # Load data for current year/semester
        self.cursor.execute('''
            SELECT course_name, grade, credits FROM courses
            WHERE student_id = 'default_student' AND year = ? AND semester = ?
            ORDER BY date_added
        ''', (self.current_year, self.current_semester))
        
        courses = self.cursor.fetchall()
        
        if courses:
            for course_name, grade, credits in courses:
                self.add_course_row(course_name, grade, str(credits))
        else:
            # Add one empty row if no data
            self.add_course_row()
        
        self.calculate_current_gpa()

    def view_all_records(self):
        # Create new window for viewing all records
        records_window = tk.Toplevel(self.root)
        records_window.title("All GPA Records")
        records_window.geometry("700x500")
        
        # Create Treeview for displaying records
        columns = ("Year", "Semester", "Semester GPA", "Cumulative GPA", "Total Credits", "Date")
        tree = ttk.Treeview(records_window, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(records_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Fetch and display data
        self.cursor.execute('''
            SELECT year, semester, semester_gpa, cumulative_gpa, total_credits, date_calculated
            FROM gpa_records 
            WHERE student_id = 'default_student'
            ORDER BY year, semester, date_calculated DESC
        ''')
        
        records = self.cursor.fetchall()
        
        for record in records:
            year, semester, sem_gpa, cum_gpa, credits, date = record
            date_formatted = date.split()[0] if date else "N/A"  # Just show date part
            tree.insert("", "end", values=(year, semester, f"{sem_gpa:.2f}", 
                                         f"{cum_gpa:.2f}", f"{credits:.1f}", date_formatted))

    def toggle_theme(self):
        if self.dark_mode:
            # Light mode
            bg_color = "#f0f0f0"
            fg_color = "black"
            self.dark_mode = False
        else:
            # Dark mode
            bg_color = "#2b2b2b"
            fg_color = "white"
            self.dark_mode = True
        
        # Update colors for widgets that support both bg and fg
        label_widgets = [
            self.semester_gpa_label, self.cumulative_gpa_label, 
            self.stats_label, self.title_label
        ]
        
        for widget in label_widgets:
            try:
                widget.config(bg=bg_color, fg=fg_color)
            except tk.TclError:
                widget.config(bg=bg_color)
        
        # Update background only for frame widgets
        frame_widgets = [self.root, self.course_frame]
        for widget in frame_widgets:
            try:
                widget.config(bg=bg_color)
            except tk.TclError:
                pass
        
        # Update canvas background
        try:
            self.canvas.config(bg=bg_color)
        except tk.TclError:
            pass

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = GPACalculator(root)
    root.mainloop()
