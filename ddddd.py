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

# Example usage
string = "The big brown fox jumps over the red bridge. The big brown rabbit eats carrots. The big brown rabbit dies. Only the small frog can swim. Only the little fox can jump."
suffix_tree = build_suffix_tree(string)
visualize(suffix_tree)
