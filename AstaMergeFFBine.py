import docx2txt
from unidecode import unidecode
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

file1_path = 'test.docx'
file2_path = 'test2.docx'
text1 = docx2txt.process(file1_path)
text2 = docx2txt.process(file2_path)

    

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
    
    filtered_words = [word for word in words if word.lower() not in stop_words]  # Eliminarea prepozițiilor
    
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

def build_suffix_tree(string):
    root = SuffixTreeNode(None)
    sentences = string.split('. ')
    for sentence in sentences:
        words = sentence.split()
        current_node = root
        for i in range(len(words)):
            word = words[i]
            if word not in current_node.children:
                current_node.children[word] = SuffixTreeNode(word)
            current_node = current_node.children[word]
    return root


def visualize(node, level=0):
    prefix = "|   " * level + "+-"
    if node.label is not None:
        print(prefix + node.label)
    for child in node.children.values():
        visualize(child, level + 1)

def calculate_similarity(tree1, tree2):
    common_nodes, total_nodes = compare_nodes(tree1, tree2)
    return common_nodes / total_nodes


def compare_nodes(node1, node2, depth=0):
    if node1 is None and node2 is None:
        return 0, 0
    
    if node1 is None:
        return 0, 1

    if node2 is None:
        return 0, 1  # Considered as 'not matched', but doesn't contribute to the total.
    
    # Only count the node if it is 4 levels deep or if it has children.
    common_nodes = int(node1.label == node2.label and (depth >= 4 or bool(node1.children) or bool(node2.children)))
    total_nodes = int(depth >= 4 or bool(node1.children))
    
    node1_children = set(node1.children.keys())
    node2_children = set(node2.children.keys())
    
    common_labels = node1_children & node2_children
    unique_labels = node1_children  # We only care about labels in node1.
    
    for label in unique_labels:
        child_common_nodes, child_total_nodes = compare_nodes(
            node1.children.get(label),
            node2.children.get(label),
            depth + 1
        )
        common_nodes += child_common_nodes
        total_nodes += child_total_nodes

    return common_nodes, total_nodes


# Example usage
textWithoutDiacr=remove_diacritics(text1)
textWithoutPrep=remove_prepositions(textWithoutDiacr)
roots = extract_roots(textWithoutPrep)
myText1=list_to_string(roots)

textWithoutDiacr=remove_diacritics(text2)
textWithoutPrep=remove_prepositions(textWithoutDiacr)
roots = extract_roots(textWithoutPrep)
myText2=list_to_string(roots)

tree1 = build_suffix_tree(myText1)
tree2 = build_suffix_tree(myText2)

visualize(tree1)
print("celalalt copac:")
visualize(tree2)
similarity = calculate_similarity(tree1, tree2)
print(f"Similarity: {similarity * 100}%")
