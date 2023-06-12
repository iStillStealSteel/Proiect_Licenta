import docx2txt
file1_path = 'test.docx'
file2_path = 'test2.docx'
text1 = docx2txt.process(file1_path)
text2 = docx2txt.process(file2_path)





class SuffixTreeNode:
    def __init__(self, label):
        self.label = label
        self.children = {}

def build_suffix_tree(string):
    root = SuffixTreeNode(None)
    words = string.split()
    current_node = root
    for i in range(len(words)):
        word = words[i]
        if word not in current_node.children:
            current_node.children[word] = SuffixTreeNode(word)
        current_node = current_node.children[word]
    return root

def calculate_common_nodes(node1, node2):
    if node1 is None or node2 is None:
        return 0
    count = 0
    for child1 in node1.children.values():
        for child2 in node2.children.values():
            if child1.label == child2.label:
                count += 1 + calculate_common_nodes(child1, child2)
    return count

def calculate_total_nodes(node):
    if node is None:
        return 0
    count = 1
    for child in node.children.values():
        count += calculate_total_nodes(child)
    return count

def calculate_newst_distance(tree1, tree2):
    common_nodes = calculate_common_nodes(tree1, tree2)
    total_nodes = calculate_total_nodes(tree1) + calculate_total_nodes(tree2)
    words_from_node = len(tree1.children) + len(tree2.children)
    newst_distance = (common_nodes * 1.0) / (total_nodes + words_from_node)
    return newst_distance

def compare_suffix_trees(tree1, tree2):
    newst_distance = calculate_newst_distance(tree1, tree2)
    similarity_percentage = (1 - newst_distance) * 100
    return similarity_percentage

# Example usage
string1 = "The big brown fox jumps over the red bridge."
string2 = "The big brown rabbit eats carrots."
string2 = "The big brown fox jumps over the red bridge."
tree1 = build_suffix_tree(string1)
tree2 = build_suffix_tree(string2)
# tree1=build_suffix_tree(text1)
# tree2=build_suffix_tree(text2)
similarity_percentage = compare_suffix_trees(tree1, tree2)
print(f"Similarity percentage: {similarity_percentage}%")
