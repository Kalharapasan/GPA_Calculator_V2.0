
# 📊 Multi-Year GPA Calculator

An advanced GPA calculator built with Python and Tkinter, supporting multiple academic years and semesters. It allows students to input course grades, credits, and calculates semester and cumulative GPAs. Data is persisted with SQLite and includes dark mode, GPA records view, and dynamic GPA updates.

![image](https://github.com/user-attachments/assets/c55a051e-df26-4010-b6a3-c9b77f7ddd9b)


---

## 🚀 Features

- 🎓 Multi-year and multi-semester GPA calculation  
- 🧮 Real-time GPA updates as you type  
- 💾 Persistent storage using SQLite  
- 🌙 Toggleable Dark Mode  
- 📈 View complete GPA history  
- 📚 Customizable grading scale (A+ to F)  
- 📊 Total credits tracker  

---

## 🖥️ Interface Preview

- Add/edit/delete courses with grade and credit input  
- Dropdown selection for academic year and semester  
- View calculated GPAs and credits immediately  
- Treeview-based GPA history display window  

---

## 🛠️ Installation

```bash
git clone https://github.com/Kalharapasan/GPA_Calculator_V2.0.git
cd gpa-calculator
python V2.0.py
```

> Requires Python 3.x installed. Tkinter and SQLite are included in standard Python.

---

## 📋 How to Use

1. Launch the app with `python V2.0.py`.
2. Select Academic Year and Semester.
3. Add your courses, grades, and credits.
4. Click "Calculate GPA" to update values.
5. Use "Save Data" to store entries.
6. View saved records with "View All Records".
7. Toggle dark/light theme with "Toggle Dark Mode".

---

## 🧮 GPA Scale

Default grade to GPA mapping:
```
A+/A: 4.0, A-: 3.7, B+: 3.3, ..., D-: 1.0, F: 0.0
```

---

## 📦 Dependencies

No external dependencies required.

- `tkinter` - GUI  
- `sqlite3` - Data storage  
- `datetime` - Timestamping  

---

## 📁 File Structure

```
├── V2.0.py          # Main application file
├── data.db          # Generated automatically to store data
```

---

## 🧑‍💻 Author

Developed by P.R.P.S.Kalhara

---

## 📄 License

This project is licensed under the MIT License.
