from suffix_tree import Tree
import docx2txt
from unidecode import unidecode
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords


       
     

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

# Exemplu de utilizare


input_text = "Am cântat pe străzi și am dansat în ploaie."
file1_path = 'test.docx'
file2_path = 'test2.docx'
text1 = docx2txt.process(file1_path)
text2 = docx2txt.process(file2_path)



textWithoutDiacr=remove_diacritics(text1)
textWithoutPrep=remove_prepositions(textWithoutDiacr)
roots = extract_roots(textWithoutPrep)
myText=list_to_string(roots)
print(myText)
#sentences = myText.split(".")
#suffix_tree = Tree()

# for sentence in sentences:
#     words = sentence.split()
#     suffix_tree.add(1,words)
    
# suffix_tree.construct_suffix_tree()

#suffix_tree.display()


#print(roots)