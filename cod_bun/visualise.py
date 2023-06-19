
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

# Example usage
# textWithoutDiacr=remove_diacritics(text1)
# textWithoutPrep=remove_prepositions(textWithoutDiacr)
# roots = extract_roots(textWithoutPrep)
# myText1=list_to_string(roots)
string = "The big brown fox jumps over the red bridge. The big brown rabbit eats carrots. The big brown rabbit dies. Only the small frog can swim. Only the little fox can jump."
tree=build_suffix_tree(string,1)
visualize(tree)
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


def compare_nodes(node1, node2, depth=0, min_depth=0):
    if node1 is None and node2 is None:
        return 0, 0
    
    if node1 is None:
        return 0, 1

    if node2 is None:
        return 0, 1  # Consideră "not matched" dar nu contribui la total.
    
    # Numără nodul numai dacă are adâncimea min_depth sau dacă are copii.
    common_nodes = int(node1.label == node2.label and (depth >= min_depth or bool(node1.children) or bool(node2.children)))
    total_nodes = int(depth >= min_depth or bool(node1.children))
    
    node1_children = set(node1.children.keys())
    node2_children = set(node2.children.keys())
    
    common_labels = node1_children & node2_children
    unique_labels = node1_children  # Ne intereseaza doar etichetele din node1
    
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



def compare_nodes_iterative(node1, node2, min_depth=0):
    stack = [(node1, node2, 0)]  # Inițializează stiva cu perechea de noduri rădăcină și adâncimea 0
    common_nodes, total_nodes = 0, 0

    while stack:
        n1, n2, depth = stack.pop()

        if n1 is None and n2 is None:
            continue

        if n1 is None or n2 is None:
            total_nodes += 1
            continue

        common_nodes += int(n1.label == n2.label and (depth >= min_depth or bool(n1.children) or bool(n2.children)))
        total_nodes += int(depth >= min_depth or bool(n1.children))
        
        node1_children = set(n1.children.keys())
        node2_children = set(n2.children.keys())

        common_labels = node1_children & node2_children

        for label in common_labels:
            stack.append((n1.children.get(label), n2.children.get(label), depth + 1))

    return common_nodes, total_nodes
