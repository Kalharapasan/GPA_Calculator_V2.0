import sqlite3
import hashlib
from typing import List, Dict, Optional

class DatabaseManager:
    """Database manager for handling user authentication and course data storage"""
    
    def __init__(self, db_name: str = "gpa_calculator.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the database with users and courses tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course_name TEXT NOT NULL,
                course_code TEXT,
                grade TEXT NOT NULL,
                credits REAL NOT NULL,
                semester TEXT,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Create index for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_courses ON courses(user_id)')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt for secure storage"""
        salt = "gpa_calc_salt_2024"  # In production, use random salt per user
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = None) -> Optional[int]:
        """Register a new user and return user ID if successful"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)", 
                (username, hashed_password, email)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None  # Username already exists
    
    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        """Authenticate user login and update last login time"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        hashed_password = self.hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?", 
            (username, hashed_password)
        )
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", 
                (user_id,)
            )
            conn.commit()
        
        conn.close()
        return user_id if result else None
    
    def save_courses(self, user_id: int, courses_data: List[Dict]) -> bool:
        """Save courses for a user (replaces existing courses)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Clear existing courses for this user
            cursor.execute("DELETE FROM courses WHERE user_id = ?", (user_id,))
            
            # Insert new courses
            for course in courses_data:
                if course['course'].strip() and course['credits']:
                    cursor.execute(
                        """INSERT INTO courses 
                           (user_id, course_name, course_code, grade, credits, semester, year) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (
                            user_id, 
                            course['course'], 
                            course.get('code', ''),
                            course['grade'], 
                            float(course['credits']),
                            course.get('semester', ''),
                            course.get('year', None)
                        )
                    )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            raise e
    
    def load_courses(self, user_id: int) -> List[Dict]:
        """Load courses for a user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT course_name, course_code, grade, credits, semester, year 
               FROM courses WHERE user_id = ? ORDER BY created_at DESC""", 
            (user_id,)
        )
        courses = cursor.fetchall()
        conn.close()
        
        return [
            {
                "course": course[0], 
                "code": course[1] or "",
                "grade": course[2], 
                "credits": str(course[3]),
                "semester": course[4] or "",
                "year": str(course[5]) if course[5] else ""
            } 
            for course in courses
        ]
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT COUNT(*) as total_courses, 
               SUM(credits) as total_credits,
               MIN(created_at) as first_course_date
               FROM courses WHERE user_id = ?""", 
            (user_id,)
        )
        stats = cursor.fetchone()
        conn.close()
        
        return {
            "total_courses": stats[0] or 0,
            "total_credits": stats[1] or 0,
            "first_course_date": stats[2]
        }
    
    def backup_user_data(self, user_id: int) -> Dict:
        """Create a backup of user's data"""
        user_data = {
            "courses": self.load_courses(user_id),
            "stats": self.get_user_stats(user_id)
        }
        return user_data