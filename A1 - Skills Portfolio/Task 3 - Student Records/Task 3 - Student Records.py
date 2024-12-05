# Import CustomTkinter for a modern and sleek GUI design
import customtkinter

# Import tkinter as tk for additional GUI components
import tkinter as tk

# Import messagebox from tkinter to display pop-up messages
from tkinter import messagebox

# PIL is essential for handling images within the application
from PIL import Image, ImageTk

# List is used for type hinting, ensuring our data structures are clear
from typing import List

# OS module assists in handling file paths and checking file existence
import os

# CSV module facilitates reading and writing student records
import csv

# Copy module enables creating deep copies of student data
import copy

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("A1 - Skills Portfolio\\Task 3 - Student Records\\Assets\\lavender.json")

# Define the Student class to manage individual student data and grade calculations
class Student:
    def __init__(self, name: str, number: int, coursework_marks: List[float], exam_mark: float):
        """
        Initialize a new Student instance with the provided details.
        
        Args:
            name (str): The student's name.
            number (int): The student's unique identification number.
            coursework_marks (List[float]): A list of coursework marks.
            exam_mark (float): The exam mark.
        """
        self.name = name
        self.number = number
        self.coursework_marks = coursework_marks
        self.total_coursework = sum(coursework_marks)
        self.exam_mark = exam_mark
        self.total_marks = self.total_coursework + self.exam_mark
        self.percentage = (self.total_marks / 160) * 100
        self.grade = self.calculate_grade()

    def calculate_grade(self) -> str:
        """Calculate the grade based on the student's percentage."""
        if self.percentage >= 70:
            return 'A'
        elif 60 <= self.percentage < 70:
            return 'B'
        elif 50 <= self.percentage < 60:
            return 'C'
        elif 40 <= self.percentage < 50:
            return 'D'
        else:
            return 'F'

def load_students(file_path: str) -> List[Student]:
    """
    Load students from the specified file and return a list of Student objects.
    """
    students_list = []
    if not os.path.exists(file_path):
        # Display an error label if the file does not exist
        error_label = customtkinter.CTkLabel(
            display_frame,
            text=f"Error: The file {file_path} does not exist.",
            justify="center",
            font=('Montserrat', 14, 'bold'),
            text_color="red"
        )
        error_label.pack(pady=20)
        return students_list

    # Open and read the CSV file containing student data
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 4:
                print(f"Skipping invalid row: {row}")
                continue
            try:
                number = int(row[0].strip())
                name = row[1].strip()
                coursework_marks = [float(mark) for mark in row[2:-1]]
                exam_mark = float(row[-1].strip())
                # Create a Student object and add it to the list
                student = Student(
                    name=name,
                    number=number,
                    coursework_marks=coursework_marks,
                    exam_mark=exam_mark
                )
                students_list.append(student)
            except ValueError as ve:
                print(f"Error parsing row {row}: {ve}")
                continue
    return students_list

def save_students(file_path: str, students_to_save: List[Student]):
    """
    Save the list of Student objects to the specified file.

    Args:
        file_path (str): The path to the student marks file.
        students_to_save (List[Student]): The list of students to save.
    """
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for student in students_to_save:
                row = [student.number, student.name] + student.coursework_marks + [student.exam_mark]
                writer.writerow(row)
    except Exception as e:
        # Display an error message if saving fails
        messagebox.showerror("Error", f"Failed to save students: {e}")

def clear_display():
    """
    Clear the display area by removing all child widgets.
    """
    for widget in display_frame.winfo_children():
        widget.forget()

def view_all_records():
    """
    Display all student records in a scrollable frame and calculate the average percentage.
    """
    clear_display()

    # Create a scrollable frame inside the display_frame
    scrollable_frame = customtkinter.CTkScrollableFrame(display_frame)
    scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

    total_percentage = 0
    for student in students:
        # Format coursework marks for display
        coursework_details = ", ".join([f"{mark}" for mark in student.coursework_marks])
        # Create a formatted record string
        record = (
            f"Name: {student.name}\n"
            f"Number: {student.number}\n"
            f"Coursework Marks: {coursework_details} (Total: {student.total_coursework})\n"
            f"Exam Mark: {student.exam_mark}\n"
            f"Overall Percentage: {student.percentage:.2f}%\n"
            f"Grade: {student.grade}\n\n"
        )
        # Create and pack a label for each student's record
        record_label = customtkinter.CTkLabel(
            scrollable_frame,
            text=record,
            justify="left",
            anchor="w",
            font=('Poppins', 16),
            text_color="white"
        )
        record_label.pack(fill="both", padx=20, pady=5)
        total_percentage += student.percentage

    # Calculate and display the average percentage
    average_percentage = total_percentage / len(students) if students else 0
    summary = (
        f"Total Students: {len(students)}\n"
        f"Average Percentage: {average_percentage:.2f}%"
    )
    summary_label = customtkinter.CTkLabel(
        scrollable_frame,
        text=summary,
        justify="left",
        anchor="w",
        font=('Montserrat', 24, 'bold'),
        text_color="white"
    )
    summary_label.pack(fill="both", padx=20, pady=10)

def view_individual_record():
    """
    Allow the user to select a student from a dropdown menu and display their individual record.
    """
    clear_display()

    def display_record():
        """
        Retrieve and display the selected student's record.
        """
        name = selected_student.get()
        student = next((s for s in students if s.name == name), None)
        if student:
            clear_display()
            coursework_details = ", ".join([f"{mark}" for mark in student.coursework_marks])
            record = (
                f"Name: {student.name}\n"
                f"Number: {student.number}\n"
                f"Coursework Marks: {coursework_details} (Total: {student.total_coursework})\n"
                f"Exam Mark: {student.exam_mark}\n"
                f"Overall Percentage: {student.percentage:.2f}%\n"
                f"Grade: {student.grade}\n"
            )
            # Create and pack a label for the selected student's record
            record_label = customtkinter.CTkLabel(
                display_frame, 
                text=record, 
                justify="left", 
                anchor="w", 
                font=('Poppins', 16),
                text_color="white")
            record_label.pack(fill="both", padx=20, pady=20)

    # Create a frame for student selection
    selection_frame = customtkinter.CTkFrame(display_frame)
    selection_frame.pack(pady=10)

    # Label for the dropdown menu
    label = customtkinter.CTkLabel(
        selection_frame, 
        text="Select Student:", 
        font=('Montserrat', 21), 
        text_color="white"
    )
    label.pack(side="left", padx=(10, 10))

    # Retrieve student names for the dropdown
    student_names = [student.name for student in students]
    if not student_names:
        # Display a message if no students are available
        no_students_label = customtkinter.CTkLabel(
            display_frame, 
            text="No students available.", 
            justify="center", 
            text_color="red", 
            font=('Montserrat', 14, 'bold'))
        no_students_label.pack(pady=20)
        return

    # Variable to hold the selected student's name
    selected_student = tk.StringVar(value=student_names[0])

    # Create the dropdown menu for student selection
    dropdown_menu = customtkinter.CTkOptionMenu(
        selection_frame, 
        values=student_names, 
        variable=selected_student,
        font=('Montserrat', 18),
        width=250,
        height=50,
    )
    dropdown_menu.pack(side="left", padx=(0, 20))

    # Button to display the selected student's record
    display_button = customtkinter.CTkButton(
        selection_frame, 
        text="Display", 
        width=100,
        height=50,
        font=('Montserrat', 18),
        command=display_record
    )
    display_button.pack(side="left")

def show_highest_score():
    """
    Display the student with the highest total marks.
    """
    clear_display()
    if not students:
        # Display a message if no student data is available
        no_data_label = customtkinter.CTkLabel(
            display_frame, 
            text="No student data available.", 
            justify="center", 
            text_color="red", 
            font=('Montserrat', 14, 'bold')
        )
        no_data_label.pack(pady=20)
        return
    # Find the student with the highest total marks
    highest_student = max(students, key=lambda s: s.total_marks)

    coursework_details = ", ".join([f"{mark}" for mark in highest_student.coursework_marks])
    record = (
        f"Name: {highest_student.name}\n"
        f"Number: {highest_student.number}\n"
        f"Coursework Marks: {coursework_details} (Total: {highest_student.total_coursework})\n"
        f"Exam Mark: {highest_student.exam_mark}\n"
        f"Overall Percentage: {highest_student.percentage:.2f}%\n"
        f"Grade: {highest_student.grade}\n"
    )

    # Create and pack a label for the highest scoring student
    record_label = customtkinter.CTkLabel(
        display_frame, 
        text=record, 
        justify="left", 
        anchor="w", 
        font=('Poppins', 16),
        text_color="white"
    )
    record_label.pack(pady=20, padx=20)

def show_lowest_score():
    """
    Display the student with the lowest total marks.
    """
    clear_display()
    if not students:
        # Display a message if no student data is available
        no_data_label = customtkinter.CTkLabel(
            display_frame, 
            text="No student data available.", 
            justify="center", 
            text_color="red", 
            font=('Montserrat', 14, 'bold')
        )
        no_data_label.pack(pady=20)
        return
    # Find the student with the lowest total marks
    lowest_student = min(students, key=lambda s: s.total_marks)

    coursework_details = ", ".join([f"{mark}" for mark in lowest_student.coursework_marks])
    record = (
        f"Name: {lowest_student.name}\n"
        f"Number: {lowest_student.number}\n"
        f"Coursework Marks: {coursework_details} (Total: {lowest_student.total_coursework})\n"
        f"Exam Mark: {lowest_student.exam_mark}\n"
        f"Overall Percentage: {lowest_student.percentage:.2f}%\n"
        f"Grade: {lowest_student.grade}\n"
    )

    # Create and pack a label for the lowest scoring student
    record_label = customtkinter.CTkLabel(
        display_frame, 
        text=record, 
        justify="left", 
        anchor="w", 
        font=('Poppins', 16),
        text_color="white"
    )
    record_label.pack(pady=20, padx=20)

def sort_student_records():
    """
    Add functionality to sort student records based on selected criteria.
    """
    clear_display()

    def perform_sort():
        """
        Sort the students based on the selected key and order.
        """
        key = sort_key_var.get()
        order = sort_order_var.get()
        reverse = True if order == "Descending" else False

        # Determine the sorting key
        if key == "Name":
            sorted_students = sorted(students, key=lambda s: s.name, reverse=reverse)
        elif key == "Number":
            sorted_students = sorted(students, key=lambda s: s.number, reverse=reverse)
        elif key == "Total Marks":
            sorted_students = sorted(students, key=lambda s: s.total_marks, reverse=reverse)
        else:
            sorted_students = students

        # Display the sorted records
        display_sorted_records(sorted_students)

    def display_sorted_records(sorted_students: List[Student]):
        """
        Display the sorted student records in a scrollable frame.
        
        Args:
            sorted_students (List[Student]): The list of sorted students.
        """
        clear_display()
        scrollable_frame = customtkinter.CTkScrollableFrame(display_frame)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

        for student in sorted_students:
            coursework_details = ", ".join([f"{mark}" for mark in student.coursework_marks])
            record = (
                f"Name: {student.name}\n"
                f"Number: {student.number}\n"
                f"Coursework Marks: {coursework_details} (Total: {student.total_coursework})\n"
                f"Exam Mark: {student.exam_mark}\n"
                f"Overall Percentage: {student.percentage:.2f}%\n"
                f"Grade: {student.grade}\n\n"
            )
            # Create and pack a label for each sorted student's record
            record_label = customtkinter.CTkLabel(
                scrollable_frame,
                text=record,
                justify="left",
                anchor="w",
                font=('Poppins', 16),
                text_color="white"
            )
            record_label.pack(fill="both", padx=20, pady=5)

    # Create a frame for sort options
    sort_frame = customtkinter.CTkFrame(display_frame)
    sort_frame.pack(pady=20)

    # Label for sort key selection
    sort_key_label = customtkinter.CTkLabel(
        sort_frame,
        text="Sort by:",
        font=('Montserrat', 18),
        text_color="white"
    )
    sort_key_label.pack(side="left", padx=(10, 10))

    # Variable and dropdown menu for selecting sort key
    sort_key_var = tk.StringVar(value="Name")
    sort_key_menu = customtkinter.CTkOptionMenu(
        sort_frame,
        values=["Name", "Number", "Total Marks"],
        variable=sort_key_var,
        font=('Montserrat', 16),
        width=200
    )
    sort_key_menu.pack(side="left", padx=(0, 20))

    # Label for sort order selection
    sort_order_label = customtkinter.CTkLabel(
        sort_frame,
        text="Order:",
        font=('Montserrat', 18),
        text_color="white"
    )
    sort_order_label.pack(side="left", padx=(0, 10))

    # Variable and dropdown menu for selecting sort order
    sort_order_var = tk.StringVar(value="Ascending")
    sort_order_menu = customtkinter.CTkOptionMenu(
        sort_frame,
        values=["Ascending", "Descending"],
        variable=sort_order_var,
        font=('Montserrat', 16),
        width=200
    )
    sort_order_menu.pack(side="left", padx=(0, 20))

    # Button to trigger the sorting process
    sort_button = customtkinter.CTkButton(
        sort_frame,
        text="Sort",
        width=300,
        height=50,
        font=('Montserrat', 16),
        command=perform_sort
    )
    sort_button.pack(side="left")

def add_student_record():
    """
    Provide a form to add a new student record.
    """
    clear_display()

    def add_student():
        """
        Add a new student to the records after validating the input.
        """
        try:
            name = name_entry.get().strip()
            number = int(number_entry.get().strip())
            coursework_marks = [float(mark.strip()) for mark in coursework_entry.get().split(',') if mark.strip() != '']
            exam_mark = float(exam_mark_entry.get().strip())

            # Validate input fields
            if not name:
                raise ValueError("Name cannot be empty.")
            if any(s.number == number for s in students):
                raise ValueError("Student number must be unique.")
            if not coursework_marks:
                raise ValueError("At least one coursework mark is required.")

            # Create and add the new student
            new_student = Student(
                name=name,
                number=number,
                coursework_marks=coursework_marks,
                exam_mark=exam_mark
            )
            students.append(new_student)
            # Inform the user of success
            messagebox.showinfo("Success", "Student record added successfully.")
            view_all_records()
        except ValueError as ve:
            # Display input errors
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            # Display any other errors
            messagebox.showerror("Error", f"Failed to add student: {e}")

    # Create a frame for the form
    form_frame = customtkinter.CTkFrame(display_frame)
    form_frame.pack(pady=20, padx=20)

    # Name input field
    name_label = customtkinter.CTkLabel(form_frame, text="Name:", font=('Montserrat', 18), text_color="white")
    name_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    name_entry = customtkinter.CTkEntry(form_frame, font=('Montserrat', 16), width=300)
    name_entry.grid(row=0, column=1, pady=10, padx=10)

    # Number input field
    number_label = customtkinter.CTkLabel(form_frame, text="Number:", font=('Montserrat', 18), text_color="white")
    number_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
    number_entry = customtkinter.CTkEntry(form_frame, font=('Montserrat', 16), width=300)
    number_entry.grid(row=1, column=1, pady=10, padx=10)

    # Coursework marks input field
    coursework_label = customtkinter.CTkLabel(form_frame, text="Coursework Marks (separated by commas):", font=('Montserrat', 18), text_color="white")
    coursework_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
    coursework_entry = customtkinter.CTkEntry(form_frame, font=('Montserrat', 16), width=300)
    coursework_entry.grid(row=2, column=1, pady=10, padx=10)

    # Exam mark input field
    exam_mark_label = customtkinter.CTkLabel(form_frame, text="Exam Mark:", font=('Montserrat', 18), text_color="white")
    exam_mark_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
    exam_mark_entry = customtkinter.CTkEntry(form_frame, font=('Montserrat', 16), width=300)
    exam_mark_entry.grid(row=3, column=1, pady=10, padx=10)

    # Button to add the student
    add_button = customtkinter.CTkButton(
        form_frame,
        text="Add Student",
        width=300,
        height=50,
        font=('Montserrat', 18, 'bold'),
        command=add_student
    )
    add_button.grid(row=4, column=0, columnspan=2, pady=20)

def delete_student_record():
    """
    Provide functionality to delete an existing student record.
    """
    clear_display()

    def delete_student():
        """
        Delete the selected student after confirmation.
        """
        name = selected_student.get()
        student = next((s for s in students if s.name == name), None)
        if student:
            # Confirm deletion with the user
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student.name}'s record?")
            if confirm:
                students.remove(student)
                messagebox.showinfo("Deleted", f"{student.name}'s record has been deleted.")
                view_all_records()
        else:
            # Display an error if the student is not found
            messagebox.showerror("Error", "Selected student not found.")

    # Create a frame for student selection
    selection_frame = customtkinter.CTkFrame(display_frame)
    selection_frame.pack(pady=20)

    # Label for the dropdown menu
    label = customtkinter.CTkLabel(
        selection_frame, 
        text="Select Student to Delete:", 
        font=('Montserrat', 18), 
        text_color="white"
    )
    label.pack(side="left", padx=(10, 10))

    # Retrieve student names for the dropdown
    student_names = [student.name for student in students]
    if not student_names:
        # Display a message if no students are available to delete
        no_students_label = customtkinter.CTkLabel(
            display_frame, 
            text="No students available to delete.", 
            justify="center", 
            text_color="red", 
            font=('Montserrat', 14, 'bold'))
        no_students_label.pack(pady=20)
        return

    # Variable to hold the selected student's name
    selected_student = tk.StringVar(value=student_names[0])

    # Create the dropdown menu for student selection
    dropdown_menu = customtkinter.CTkOptionMenu(
        selection_frame, 
        values=student_names, 
        variable=selected_student,
        font=('Montserrat', 16),
        width=250
    )
    dropdown_menu.pack(side="left", padx=(0, 20))

    # Button to delete the selected student
    delete_button = customtkinter.CTkButton(
        selection_frame, 
        text="Delete", 
        width=300,
        height=50,
        font=('Montserrat', 16, 'bold'),
        command=delete_student
    )
    delete_button.pack(side="left")

def update_student_record():
    """
    Provide functionality to update an existing student record.
    """
    clear_display()

    def select_student():
        """
        Select a student and display fields to update their information.
        """
        name = selected_student.get()
        student = next((s for s in students if s.name == name), None)
        if student:
            # Disable the select button while updating
            update_select_button.configure(state="disabled")
            display_update_fields(student)
        else:
            # Display an error if the student is not found
            messagebox.showerror("Error", "Selected student not found.")

    def display_update_fields(student: Student):
        """
        Display input fields pre-filled with the selected student's data for updating.
        
        Args:
            student (Student): The student to update.
        """
        update_frame = customtkinter.CTkFrame(display_frame)
        update_frame.pack(pady=20, padx=20)

        def update_record():
            """
            Update the student's record with the new input data.
            """
            try:
                new_name = name_entry.get().strip()
                new_number = int(number_entry.get().strip())
                coursework_marks = [float(mark.strip()) for mark in coursework_entry.get().split(',') if mark.strip() != '']
                exam_mark = float(exam_mark_entry.get().strip())

                # Validate input fields
                if not new_name:
                    raise ValueError("Name cannot be empty.")
                if new_number != student.number and any(s.number == new_number for s in students):
                    raise ValueError("Student number must be unique.")
                if not coursework_marks:
                    raise ValueError("At least one coursework mark is required.")

                # Update the student's information
                student.name = new_name
                student.number = new_number
                student.coursework_marks = coursework_marks
                student.total_coursework = sum(coursework_marks)
                student.exam_mark = exam_mark
                student.total_marks = student.total_coursework + student.exam_mark
                student.percentage = (student.total_marks / 160) * 100
                student.grade = student.calculate_grade()

                # Inform the user of success and refresh the records view
                messagebox.showinfo("Success", "Student record updated successfully.")
                view_all_records()
                # Re-enable the select button
                update_select_button.configure(state="normal")
            except ValueError as ve:
                # Display input errors
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                # Display any other errors
                messagebox.showerror("Error", f"Failed to update student: {e}")
                update_select_button.configure(state="normal")

        # Name input field
        name_label = customtkinter.CTkLabel(update_frame, text="Name:", font=('Montserrat', 18), text_color="white")
        name_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        name_entry = customtkinter.CTkEntry(update_frame, font=('Montserrat', 16), width=300)
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        name_entry.insert(0, student.name)

        # Number input field
        number_label = customtkinter.CTkLabel(update_frame, text="Number:", font=('Montserrat', 18), text_color="white")
        number_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        number_entry = customtkinter.CTkEntry(update_frame, font=('Montserrat', 16), width=300)
        number_entry.grid(row=1, column=1, pady=10, padx=10)
        number_entry.insert(0, str(student.number))

        # Coursework marks input field
        coursework_label = customtkinter.CTkLabel(update_frame, text="Coursework Marks (comma separated):", font=('Montserrat', 18), text_color="white")
        coursework_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        coursework_entry = customtkinter.CTkEntry(update_frame, font=('Montserrat', 16), width=300)
        coursework_entry.grid(row=2, column=1, pady=10, padx=10)
        coursework_entry.insert(0, ", ".join([str(mark) for mark in student.coursework_marks]))

        # Exam mark input field
        exam_mark_label = customtkinter.CTkLabel(update_frame, text="Exam Mark:", font=('Montserrat', 18), text_color="white")
        exam_mark_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        exam_mark_entry = customtkinter.CTkEntry(update_frame, font=('Montserrat', 16), width=300)
        exam_mark_entry.grid(row=3, column=1, pady=10, padx=10)
        exam_mark_entry.insert(0, str(student.exam_mark))

        # Button to update the student's record
        update_button = customtkinter.CTkButton(
            update_frame,
            text="Update",
            width=300,
            height=50,
            font=('Montserrat', 18, 'bold'),
            command=update_record
        )
        update_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Create a frame for student selection
    selection_frame = customtkinter.CTkFrame(display_frame)
    selection_frame.pack(pady=20)

    # Label for the dropdown menu
    label = customtkinter.CTkLabel(
        selection_frame, 
        text="Select Student to Update:", 
        font=('Montserrat', 18), 
        text_color="white"
    )
    label.pack(side="left", padx=(10, 10))

    # Retrieve student names for the dropdown
    student_names = [student.name for student in students]
    if not student_names:
        # Display a message if no students are available to update
        no_students_label = customtkinter.CTkLabel(
            display_frame, 
            text="No students available to update.", 
            justify="center", 
            text_color="red", 
            font=('Montserrat', 14, 'bold'))
        no_students_label.pack(pady=20)
        return

    # Variable to hold the selected student's name
    selected_student = tk.StringVar(value=student_names[0])

    # Create the dropdown menu for student selection
    dropdown_menu = customtkinter.CTkOptionMenu(
        selection_frame, 
        values=student_names, 
        variable=selected_student,
        font=('Montserrat', 16),
        width=250
    )
    dropdown_menu.pack(side="left", padx=(0, 20))

    # Button to select and update the student
    update_select_button = customtkinter.CTkButton(
        selection_frame, 
        text="Select", 
        width=300,
        height=50,
        font=('Montserrat', 16, 'bold'),
        command=select_student
    )
    update_select_button.pack(side="left")

def main_menu_additions():
    """
    Add additional buttons to the main menu for sorting, adding, deleting, and updating records.
    """
    # Create a new frame for additional buttons below the existing button_frame
    additional_button_frame = customtkinter.CTkFrame(main_frame)
    additional_button_frame.pack(anchor="n", pady=(10, 10))

    # Button to sort records
    sort_button = customtkinter.CTkButton(
        additional_button_frame,
        text="Sort Records",
        width=300,
        height=50,
        font=('Montserrat', 18, 'bold'),
        text_color="white",
        command=sort_student_records
    )
    sort_button.pack(side="left", padx=(0,10))

    # Button to add a new record
    add_button = customtkinter.CTkButton(
        additional_button_frame,
        text="Add Record",
        width=300,
        height=50,
        font=('Montserrat', 18, 'bold'),
        text_color="white",
        command=add_student_record
    )
    add_button.pack(side="left", padx=10)

    # Button to delete a record
    delete_button = customtkinter.CTkButton(
        additional_button_frame,
        text="Delete Record",
        width=300,
        height=50,
        font=('Montserrat', 18, 'bold'),
        text_color="white",
        command=delete_student_record
    )
    delete_button.pack(side="left", padx=10)

    # Button to update a record
    update_button = customtkinter.CTkButton(
        additional_button_frame,
        text="Update Record",
        width=300,
        height=50,
        font=('Montserrat', 18, 'bold'),
        text_color="white",
        command=update_student_record
    )
    update_button.pack(side="left", padx=(10,0))

def on_close():
    """
    Restore the original student records upon closing the application.
    """
    try:
        save_students(file_path, original_students)
    except Exception as e:
        # Display an error message if restoration fails
        messagebox.showerror("Error", f"Failed to restore original records: {e}")
    finally:
        # Destroy the main window to close the application
        root.destroy()

# Define the path to the student marks file
file_path = os.path.join(
    "A1 - Skills Portfolio",
    "Task 3 - Student Records",
    "Assets",
    "studentMarks.txt"
)

# Load students from the specified file
students: List[Student] = load_students(file_path)

# Create a deep copy of the original students to restore later if needed
original_students = copy.deepcopy(students)

# Initialize the main application window with CustomTkinter
root = customtkinter.CTk(fg_color="black")
root.geometry("1366x768")  # Set the window size
root.resizable(False, False)  # Make the window non-resizable
root.title("Student Records")  # Set the window title

# Create the title frame which displays the application title and start button
title_frame = customtkinter.CTkFrame(root)
main_frame = customtkinter.CTkFrame(root)

# Define the path to the background image
image_path = os.path.join(
    "A1 - Skills Portfolio",
    "Task 3 - Student Records",
    "Assets",
    "AcademiaPro.png"
)

# Load and resize the image to match the title_frame dimensions
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image
background_label = customtkinter.CTkLabel(
    title_frame,
    image=background_photo,
    text="",  # No text needed for the background
)
background_label.image = background_photo  # Keep a reference to prevent garbage collection
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch the image to fit the frame

# Start button to transition from the title frame to the main frame
title_start = customtkinter.CTkButton(
    title_frame,
    text="START",
    width=200,
    height=100,
    font=('Montserrat', 32, 'bold'),
    text_color="white",
    command=lambda: [title_frame.forget(), main_frame.pack(expand=True, fill="both")]
)
title_start.pack(anchor="center", side="bottom", pady=(0,50))
title_frame.pack(expand=True, fill="both")  # Display the title frame initially

# Label for the main frame header
main_header = customtkinter.CTkLabel(
    main_frame,
    text="Student Manager",
    font=('Montserrat', 38, 'bold'),
    text_color="white"
) 
main_header.pack(pady=(10,5))

# Frame to hold the existing and additional buttons
button_frame = customtkinter.CTkFrame(main_frame)
button_frame.pack(anchor="n", pady=(10))

# Button to view all student records
view_all = customtkinter.CTkButton(
    button_frame,
    text="View All Student Records",
    width=300,
    height=50,
    font=('Montserrat', 18, 'bold'),
    text_color="white",
    command=view_all_records
)
view_all.pack(side="left", padx=(0, 10))

# Button to view an individual student's record
view_individual = customtkinter.CTkButton(
    button_frame,
    text="View Individual Record",
    width=300,
    height=50,
    font=('Montserrat', 18, 'bold'),
    text_color="white",
    command=view_individual_record
)
view_individual.pack(side="left", padx=10)

# Button to show the highest scoring student
show_highest = customtkinter.CTkButton(
    button_frame,
    text="Show Highest Score",
    width=300,
    height=50,
    font=('Montserrat', 18, 'bold'),
    text_color="white",
    command=show_highest_score
)
show_highest.pack(side="left", padx=10)

# Button to show the lowest scoring student
show_lowest = customtkinter.CTkButton(
    button_frame,
    text="Show Lowest Score",
    width=300,
    height=50,
    font=('Montserrat', 18, 'bold'),
    text_color="white",
    command=show_lowest_score
)
show_lowest.pack(side="left", padx=(10, 0))

# Add new menu options (Sort, Add, Delete, Update) to the main menu
main_menu_additions()

# Frame where the records and other dynamic content will be displayed
display_frame = customtkinter.CTkFrame(main_frame)
display_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Initialize display_frame with a welcome message
welcome_label = customtkinter.CTkLabel(
    display_frame,
    text="Welcome to the Student Records Manager!\nPlease select an option above to proceed.",
    justify="center",
    font=('Montserrat', 32),
    text_color="white"
)
welcome_label.pack(expand=True)

# Set the protocol for window close to restore original records
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the main event loop
root.mainloop()