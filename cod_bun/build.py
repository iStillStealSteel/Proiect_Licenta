import docx2txt
from unidecode import unidecode
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pickle


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


def save_tree(tree, filename):
    with open(filename, 'wb') as f:
        pickle.dump(tree, f)

# Example usage
textWithoutDiacr=remove_diacritics(text1)
textWithoutPrep=remove_prepositions(textWithoutDiacr)
roots = extract_roots(textWithoutPrep)
myText1=list_to_string(roots)

# textWithoutDiacr=remove_diacritics(text2)
# textWithoutPrep=remove_prepositions(textWithoutDiacr)
# roots = extract_roots(textWithoutPrep)
# myText2=list_to_string(roots)

tree1 = build_suffix_tree(myText1, 2)
#tree2 = build_suffix_tree(myText2, 2)

save_tree(tree1, 'cod_bun/Inginerie_test/tree1.pkl')


visualize(tree1)
print("celalalt copac:")
#visualize(tree2)
