import docx2txt

import graphviz


class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class SuffixTree:
    def __init__(self):
        self.root = SuffixTreeNode()

    def add_suffix(self, suffix):
        current_node = self.root

        for char in suffix:
            if char not in current_node.children:
                current_node.children[char] = SuffixTreeNode()
            current_node = current_node.children[char]

        current_node.is_end_of_word = True

    def construct_suffix_tree(self, text):
        text += '$'
        text_length = len(text)

        for i in range(text_length):
            current_node = self.root
            for j in range(i, text_length):
                char = text[j]
                if char not in current_node.children:
                   current_node.children[char] = SuffixTreeNode()
                current_node = current_node.children[char]
            current_node.is_end_of_word = True
            
    def display(self):
        dot = graphviz.Digraph()
        stack = [(self.root, '')]

        while stack:
            current_node, parent_node_name = stack.pop()
            for char, child_node in current_node.children.items():
                child_node_name = parent_node_name + char
                dot.node(child_node_name)
                dot.edge(parent_node_name, child_node_name, label=char)
                stack.append((child_node, child_node_name))

        dot.render('suffix_tree', format='png', view=True)
        
    def count_suffixes(self):
        count = 0
        stack = [self.root]

        while stack:
            current_node = stack.pop()
            if current_node.is_end_of_word:
                count += 1
            stack.extend(current_node.children.values())

        return count
def compare_files(file1_path, file2_path):
    # Read the contents of both files
    text1 = docx2txt.process(file1_path)
    text2 = docx2txt.process(file2_path)

    # Build a suffix tree for the first file
    suffix_tree = SuffixTree()
    suffix_tree.construct_suffix_tree(text1)

    # Display the suffix tree
    #suffix_tree.display()

    # Count the number of suffixes in the first file's suffix tree
    total_suffixes = suffix_tree.count_suffixes()

    # Traverse the suffix tree and search for each suffix in the second file
    matches = 0

    for i in range(len(text1)):
        suffix = text1[i:]
        if suffix in text2:
            matches += 1

    # Calculate match percentage
    match_percentage = (matches / total_suffixes) * 100

    return match_percentage


# Example usage
file1_path = 'test.docx'
file2_path = 'test2.docx'
match_percentage = compare_files(file1_path, file2_path)
print(f"Match percentage: {match_percentage}%")
