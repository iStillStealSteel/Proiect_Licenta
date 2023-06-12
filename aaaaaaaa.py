import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class PlagiarismChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Plagiarism Checker')
        self.geometry('300x200')
        
        self.filename = tk.StringVar()
        self.topic = tk.StringVar()
        self.plagiarism_percentage = tk.StringVar()

        self.create_widgets()
    
    def create_widgets(self):
        # Select File button
        self.select_file_button = ttk.Button(self, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # Dropdown for topic selection
        self.topic_label = ttk.Label(self, text="Select Topic:")
        self.topic_label.pack()
        self.topic_dropdown = ttk.Combobox(self, textvariable=self.topic)
        self.topic_dropdown['values'] = ('Topic 1', 'Topic 2', 'Topic 3')  # TODO: populate with real topics
        self.topic_dropdown.pack(pady=10)

        # Compare button
        self.compare_button = ttk.Button(self, text="Compare", command=self.compare)
        self.compare_button.pack(pady=10)

        # Save button
        self.save_button = ttk.Button(self, text="Save", command=self.save)
        self.save_button.pack(pady=10)

        # Display plagiarism percentage
        self.result_label = ttk.Label(self, textvariable=self.plagiarism_percentage)
        self.result_label.pack(pady=10)

    def select_file(self):
        self.filename.set(filedialog.askopenfilename())
    
    def compare(self):
        # TODO: Use the self.filename.get() and self.topic.get() values to perform the comparison
        # Set the result to self.plagiarism_percentage
        # For example:
        # result = compare(self.filename.get(), self.topic.get())
        self.plagiarism_percentage.set("TODO: Compare and calculate the plagiarism percentage")

    def save(self):
        # TODO: Implement the saving functionality
        messagebox.showinfo("Info", "Saved")

app = PlagiarismChecker()
app.mainloop()
