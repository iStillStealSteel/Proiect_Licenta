#ALMOST GOOD

class SuffixTreeNode:
    def __init__(self, key):
        self.key = key
        self.children = []

class SuffixTree:
    def __init__(self, sentence):
        self.root = SuffixTreeNode('')
        self.build_suffix_tree(sentence)

    def build_suffix_tree(self, sentence):
        words = sentence.split()
        for i in range(len(words)):
            suffix = words[i:]
            current = self.root
            for word in suffix:
                found_child = False
                for child in current.children:
                    if child.key == word:
                        current = child
                        found_child = True
                        break
                if not found_child:
                    new_node = SuffixTreeNode(word)
                    current.children.append(new_node)
                    current = new_node

    def visualize(self):
        def print_node(node, level=0):
            prefix = "|   " * level + "+-"
            print(prefix + node.key)
            for child in node.children:
                print_node(child, level + 1)

        for child in self.root.children:
            print_node(child)
            
            
# Example usage:
suffix_tree = SuffixTree("The big brown fox jumps over the red bridge. The big brown rabbit eats carrots")
suffix_tree.visualize()
