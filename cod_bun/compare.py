import docx2txt
from unidecode import unidecode
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pickle
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os


# file1_path = 'test.docx'
# file2_path = 'test2.docx'
# text1 = docx2txt.process(file1_path)
# text2 = docx2txt.process(file2_path)

class PlagiarismChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Plagiarism Checker')
        self.geometry('300x300')
        
        self.filename = tk.StringVar()
        self.topic = tk.StringVar()
        self.plagiarism_results = tk.StringVar()
        
        self.min_depth = tk.StringVar(value='1')  # Set default value

        self.create_widgets()
    
    def create_widgets(self):
        # Select File button
        self.select_file_button = ttk.Button(self, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)
        
        # Label to display selected filename
        self.filename_label = ttk.Label(self, textvariable=self.filename)
        self.filename_label.pack(pady=[0,10])
        
        # Dropdown for topic selection
        self.topic_label = ttk.Label(self, text="Select Topic:")
        self.topic_label.pack(pady=[10,0])

        # Get topic values from subdirectories of dataBase folder
        database_directory = "dataBase"
        self.topic_dropdown = ttk.Combobox(self, textvariable=self.topic)
        self.topic_dropdown['values'] = [d for d in os.listdir(database_directory) if os.path.isdir(os.path.join(database_directory, d))]
        self.topic_dropdown.pack(pady=10)

        # Dropdown for min_depth selection
        self.min_depth_label = ttk.Label(self, text="Select Min Depth:")
        self.min_depth_label.pack()
        self.min_depth_dropdown = ttk.Combobox(self, textvariable=self.min_depth)
        self.min_depth_dropdown['values'] = list(range(1, 9))  # 1 to 8 inclusive
        self.min_depth_dropdown.pack(pady=10)
        
        # Compare button
        self.compare_button = ttk.Button(self, text="Compare", command=self.compare)
        self.compare_button.pack(pady=10)

        # Save button
        self.save_button = ttk.Button(self, text="Save", command=self.save)
        self.save_button.pack(pady=10)

        # Display plagiarism results
        self.result_label = ttk.Label(self, textvariable=self.plagiarism_results)
        self.result_label.pack(pady=10)
        
        
        
    def select_file(self):
        self.filename.set(filedialog.askopenfilename())
    
    def compare(self):
     # Get selected topic directory
        topic_directory = os.path.join("dataBase", self.topic.get())

    # Make sure the directory exists
        if not os.path.isdir(topic_directory):
            self.plagiarism_results.set("No data for this topic.")
            return

    # Prepare the document to be checked
        text = docx2txt.process(self.filename.get())
        textWithoutDiacr =remove_diacritics(text)
        textWithoutPrep = remove_prepositions(textWithoutDiacr)
        textWithCorrectPunct=replace_punctuation(textWithoutPrep)
        roots = extract_roots(textWithCorrectPunct)
        myText = list_to_string(roots)

    # Build the tree for the document to be checked
        check_tree = build_suffix_tree(myText, 2)

    # Get a list of all .pkl files in the topic directory
        suffix_tree_files = [f for f in os.listdir(topic_directory) if f.endswith('_st.pkl')]

        if not suffix_tree_files:
            self.plagiarism_results.set("No data for this topic.")
            messagebox.showinfo("Info", "No files to compare with")
            return

    # Check if min_depth has a valid value
        try:
            min_depth = int(self.min_depth.get())
        except ValueError:
            self.plagiarism_results.set("Please select a valid min depth.")
            messagebox.showinfo("Error", "Please select a valid min depth.")
            return
    # Compare with each saved suffix tree
        results = []
        for filename in suffix_tree_files:
            try:
            # Load the saved tree
                print(os.path.join(topic_directory, filename))
                saved_tree = load_tree(os.path.join(topic_directory, filename))
                
            # Calculate the similarity
                similarity = calculate_similarity(check_tree, saved_tree, min_depth)

            # Add the result to the list
                results.append((filename, similarity))
                #print((filename, similarity))
            except Exception as e:
                results.append((filename, str(e)))

    # Display the results
        result_text = "\n".join(f"{filename}: {similarity*100:.2f}%" if isinstance(similarity, float) else f"{filename}: {similarity}" for filename, similarity in results)
        self.plagiarism_results.set(result_text)
        #print(result_text)
        messagebox.showinfo("Info", result_text)


    def save(self):
        text = docx2txt.process(self.filename.get())
        textWithoutDiacr = remove_diacritics(text)
        textWithoutPrep = remove_prepositions(textWithoutDiacr)
        roots = extract_roots(textWithoutPrep)
        myText = list_to_string(roots)

        tree = build_suffix_tree(myText, 2)

        # Replace with your actual database directory
        database_directory = "dataBase"
        topic_directory = os.path.join(database_directory, self.topic.get())
        if not os.path.exists(topic_directory):
            os.makedirs(topic_directory)
        
        path = os.path.join(topic_directory, os.path.basename(self.filename.get()) + "_st.pkl")
        save_tree(tree, path)

        messagebox.showinfo("Info", f"Saved to {path}")


def replace_punctuation(text):
    punctuation = ['!', '?', ';']
    for p in punctuation:
        text = text.replace(p, '.')
    return text

def list_to_string(lst):
    string_repr = ' '.join(str(element) for element in lst)
    return string_repr

def remove_diacritics(text):
    text = unidecode(text)
    return text

def remove_prepositions(text):
    nltk.download('stopwords')  # Descarcă lista de stop words (inclusiv prepoziții)
    stop_words = set(stopwords.words('romanian'))
    stop_words.add(',')
    words = nltk.word_tokenize(text)  # Tokenizare în cuvinte
    
    # Eliminarea prepozițiilor
    filtered_words = [word for word in words if word.lower() not in stop_words]  
    
    return ' '.join(filtered_words)  # Returnarea șirului de caractere fără prepoziții

def extract_roots(text):
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


def visualize(node, level=0):
    prefix = "|   " * level + "+-"
    if node.label is not None:
        print(prefix + node.label)
    for child in node.children.values():
        visualize(child, level + 1)

def calculate_similarity(tree1, tree2, min_depth):
    common_nodes, total_nodes = compare_nodes(tree1, tree2, min_depth=min_depth)
    print(common_nodes / total_nodes)
    return common_nodes / total_nodes

def compare_nodes(node1, node2, depth=0, min_depth=0):
    if node1 is None and node2 is None:
        return 0, 0
    
    if node1 is None:
        return 0, 1

    if node2 is None:
        return 0, 1  # Considered as 'not matched', but doesn't contribute to the total.
    
    # Only count the node if it is min_depth levels deep or if it has children.
    common_nodes = int(node1.label == node2.label and (depth >= min_depth or bool(node1.children) or bool(node2.children)))
    total_nodes = int(depth >= min_depth or bool(node1.children))
    
    node1_children = set(node1.children.keys())
    node2_children = set(node2.children.keys())
    
    common_labels = node1_children & node2_children
    unique_labels = node1_children  # We only care about labels in node1.
    
    for label in unique_labels:
        child_common_nodes, child_total_nodes = compare_nodes(
            node1.children.get(label),
            node2.children.get(label),
            depth + 1,
            min_depth
        )
        common_nodes += child_common_nodes
        total_nodes += child_total_nodes

    return common_nodes, total_nodes

def load_tree(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
def save_tree(tree, filename):
    with open(filename, 'wb') as f:
        pickle.dump(tree, f)

app = PlagiarismChecker()
app.mainloop()
# Example usage
# textWithoutDiacr=remove_diacritics(text1)
# textWithoutPrep=remove_prepositions(textWithoutDiacr)
# roots = extract_roots(textWithoutPrep)
# myText1=list_to_string(roots)

# textWithoutDiacr=remove_diacritics(text2)
# textWithoutPrep=remove_prepositions(textWithoutDiacr)
# roots = extract_roots(textWithoutPrep)
# myText2=list_to_string(roots)

# #tree1 = build_suffix_tree(myText1)
# tree2 = build_suffix_tree(myText2,2)


# tree1 = load_tree('tree1.pkl')

# visualize(tree1)
# print("celalalt copac:")
# visualize(tree2)
# similarity = calculate_similarity(tree1, tree2)
# print(f"Similarity: {similarity * 100}%")





# def compare_nodes(node1, node2, depth=0):
#     if node1 is None and node2 is None:
#         return 0, 0
    
#     if node1 is None:
#         return 0, 1

#     if node2 is None:
#         return 0, 1  # Considered as 'not matched', but doesn't contribute to the total.
    
#     # Only count the node if it is 4 levels deep or if it has children.
#     common_nodes = int(node1.label == node2.label and (depth >= 4 or bool(node1.children) or bool(node2.children)))
#     total_nodes = int(depth >= 4 or bool(node1.children))
    
#     node1_children = set(node1.children.keys())
#     node2_children = set(node2.children.keys())
    
#     common_labels = node1_children & node2_children
#     unique_labels = node1_children  # We only care about labels in node1.
    
#     for label in unique_labels:
#         child_common_nodes, child_total_nodes = compare_nodes(
#             node1.children.get(label),
#             node2.children.get(label),
#             depth + 1
#         )
#         common_nodes += child_common_nodes
#         total_nodes += child_total_nodes

#     return common_nodes, total_nodes