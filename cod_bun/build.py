import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import docx2txt
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from unidecode import unidecode
import nltk
import pickle

class SuffixTreeCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Suffix Tree Creator')
        self.geometry('300x200')

        self.filename = tk.StringVar()
        self.topic = tk.StringVar()

        self.create_widgets()
        self.populate_topics()

    def create_widgets(self):
        # Select File button
        self.select_file_button = ttk.Button(self, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # Dropdown for topic selection
        self.topic_label = ttk.Label(self, text="Select Topic:")
        self.topic_label.pack()
        self.topic_dropdown = ttk.Combobox(self, textvariable=self.topic)
        self.topic_dropdown.pack(pady=10)

        # Add Topic button
        self.add_topic_button = ttk.Button(self, text="Add Topic", command=self.add_topic)
        self.add_topic_button.pack(pady=10)

        # Save button
        self.save_button = ttk.Button(self, text="Save", command=self.save)
        self.save_button.pack(pady=10)

    def select_file(self):
        self.filename.set(filedialog.askopenfilename())

    def add_topic(self):
        # prompt user to enter new topic name
        new_topic = simpledialog.askstring("Add Topic", "Enter new topic name")

        if new_topic is not None and new_topic.strip() != "":
            database_directory = "cod_bun/dataBase"
            new_topic_directory = os.path.join(database_directory, new_topic)
            if not os.path.exists(new_topic_directory):
                os.makedirs(new_topic_directory)
            self.populate_topics()

    def populate_topics(self):
        database_directory = "cod_bun/dataBase"
        if not os.path.exists(database_directory):
            os.makedirs(database_directory)
        self.topic_dropdown['values'] = next(os.walk(database_directory))[1]  # get all directories in database_directory

    def save(self):
        text = docx2txt.process(self.filename.get())
        textWithoutDiacr = self.remove_diacritics(text)
        textWithoutPrep = self.remove_prepositions(textWithoutDiacr)
        roots = self.extract_roots(textWithoutPrep)
        myText = self.list_to_string(roots)

        tree = build_suffix_tree(myText, 2)

        # Replace with your actual database directory
        database_directory = "cod_bun/dataBase"
        topic_directory = os.path.join(database_directory, self.topic.get())
        if not os.path.exists(topic_directory):
            os.makedirs(topic_directory)
        
        path = os.path.join(topic_directory, os.path.basename(self.filename.get()) + "_st.pkl")
        save_tree(tree, path)

        messagebox.showinfo("Info", f"Saved to {path}")


    def list_to_string(self, lst):
        string_repr = ' '.join(str(element) for element in lst)
        return string_repr

    def remove_diacritics(self, text):
        text = unidecode(text)
        return text

    def remove_prepositions(self, text):
        nltk.download('stopwords')  # Download the list of stop words (including prepositions)
        stop_words = set(stopwords.words('romanian'))
        stop_words.add(',')
        words = nltk.word_tokenize(text)  # Tokenize into words

        filtered_words = [word for word in words if word.lower() not in stop_words]  # Remove prepositions

        return ' '.join(filtered_words)  # Return the string of characters without prepositions

    def extract_roots(self, text):
        stemmer = SnowballStemmer('romanian')
        words = nltk.word_tokenize(text)
        roots = [stemmer.stem(word) for word in words]
        return roots

class SuffixTreeNode:
    def __init__(self, label):
        self.label = label
        self.children = {}
        
def get_ngrams(input_list, n):
        return [' '.join(input_list[i:i+n]) for i in range(len(input_list)-(n-1))]

def build_suffix_tree(string, n):
    root = SuffixTreeNode(None)
    sentences = string.split('. ')
    for sentence in sentences:
        words = sentence.split()
        ngrams = get_ngrams(words, n)
        current_node = root
        for i in range(len(ngrams)):
            ngram = ngrams[i]
            if ngram not in current_node.children:
                current_node.children[ngram] = SuffixTreeNode(ngram)
            current_node = current_node.children[ngram]
    return root

def save_tree(tree, filename):
    with open(filename, 'wb') as f:
        pickle.dump(tree, f)


app = SuffixTreeCreator()
app.mainloop()
