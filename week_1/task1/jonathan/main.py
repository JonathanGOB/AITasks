class Node:

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        self.path = []

    def add_child(self, child):
        self.children.append(child)
        child.path = self.path + [self.data]
        return child


def gwcgenerator(parent, found): # O(b^d)
    data = parent.data.split('|')
    for e in data[0]:
        if move_right(parent.data, e) in parent.path:
            continue
        child = parent.add_child(Node(move_right(parent.data, e), parent))
        if check_failure(child.data):
            continue
        if len(child.data.split('|')[1]) == 4:
            found.append(child)
            continue
        child_data = child.data.split('|')
        for i in child_data[1]:
            if move_left(child.data, i) in child.path:
                continue
            child1 = child.add_child(Node(move_left(child.data, i), child))
            if not check_failure(child1.data):
                gwcgenerator(child1, found)
    return found


def print_path(node):
    if node.parent is not None:
        print_path(node.parent)
    print("→ " + node.data, end=' ')


def check_failure(string):
    death = ["CG", "GW", "CGW"]
    string = string.split('|')
    for e in death:
        if e == string[0] or e == string[1]:
            return True
    return False


def move_right(whole_string, character):
    position = whole_string.find(character)
    whole_string = whole_string[:position] + whole_string[position + 1:] + character
    position = whole_string.find("F")
    whole_string = whole_string[:position] + whole_string[position + 1:] + "F"
    whole_string = ''.join(sorted(list(whole_string.split("|")[0]))) + "|" + ''.join(sorted(list(whole_string.split("|")[1])))
    return whole_string


def move_left(whole_string, character):
    position = whole_string.find(character)
    whole_string = character + whole_string[:position] + whole_string[position + 1:]
    position = whole_string.find("F")
    whole_string = "F" + whole_string[:position] + whole_string[position + 1:]
    whole_string = ''.join(sorted(list(whole_string.split("|")[0]))) + "|" + ''.join(
        sorted(list(whole_string.split("|")[1])))
    return whole_string


if __name__ == "__main__":
    found = gwcgenerator(Node('CFGW|'), [])
    for e in range(len(found)):
        print()
        print_path(found[e])
