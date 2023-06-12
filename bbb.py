class Node:
    def __init__(self, sub="", children=None):
        self.sub = sub
        self.ch = children or []

class SuffixTree:
    def __init__(self, strings):
        self.nodes = [Node()]
        if isinstance(strings, str):
            strings = strings.split(".")
        for string in strings:
            words = string.strip().split(" ")
            for i in range(len(words)):
                self.addSuffix(words[i:], i)

    def addSuffix(self, suf, word_index):
        n = 0
        i = 0
        while i < len(suf):
            b = suf[i]
            x2 = 0
            while True:
                children = self.nodes[n].ch
                if x2 == len(children):
                    # No matching child, remainder of suf becomes new node
                    n2 = len(self.nodes)
                    self.nodes.append(Node(suf[i:], []))
                    self.nodes[n].ch.append(n2)
                    return
                n2 = children[x2]
                if self.nodes[n2].sub[0] == b:
                    break
                x2 += 1

            # Find the prefix of the remaining suffix in common with the child
            sub2 = self.nodes[n2].sub
            j = 0
            while j < len(sub2):
                if suf[i + j] != sub2[j]:
                    # Split n2
                    n3 = n2
                    # Create a new node for the part in common
                    n2 = len(self.nodes)
                    self.nodes.append(Node(sub2[:j], [n3]))
                    self.nodes[n3].sub = sub2[j:]  # The old node loses the part in common
                    self.nodes[n].ch[x2] = n2
                    break  # Continue down the tree
                j += 1
            i += j  # Advance past the part in common
            n = n2  # Continue down the tree

        # Set the suffix and word index for the final node
        self.nodes[n].sub = suf[i:]
        self.nodes[n].word_index = word_index
        
    def visualize(self):
        def printNode(node, level=0):
            prefix = "|   " * level + "+-"
            if node.sub:
                print(prefix + "+ " + str(node.sub))

            for child in node.ch:
                printNode(self.nodes[child], level + 1)

        printNode(self.nodes[0])


# Example usage:
suffix_tree = SuffixTree("The big brown fox jumps over the red bridge. The big brown rabbit eats carrots")
suffix_tree.visualize()
