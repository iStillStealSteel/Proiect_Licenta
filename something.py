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
        # Add a special character to mark the end of the sentence
        end_char = "$"
        if end_char not in current_node.children:
            current_node.children[end_char] = SuffixTreeNode(end_char)
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

# Example usage
string1 = "The big brown fox jumps over the red bridge. The big brown rabbit eats carrots. Only the small frog can swim. Only the little fox can jump."
suffix_tree1 = build_suffix_tree(string1)

# Process the second document and obtain its text content
# Let's assume the second document is stored in a variable called 'text2'
text2 = "The quick brown fox jumps over the lazy dog. The lazy dog barks at the moon."

suffix_tree2 = build_suffix_tree(text2)

newst_distance = calculate_newst_distance(suffix_tree1, suffix_tree2)
similarity_percentage = (1 - newst_distance) * 100
print(f"Similarity percentage: {similarity_percentage}%")
