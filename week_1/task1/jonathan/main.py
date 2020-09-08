# Using Postorder (Left, Right, Root)
class Node:
    data = None
    parent = None
    children = []

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)
        return child

    def get_children(self):
        return_list = []
        for e in self.children:
            return_list.append(e.data)
        return return_list

found = []

def gwcgenerator(parent):
    data = parent.data.split('|')
    for e in range(len(data[0]) - 1):
        if move_right(parent.data, data[0][e + 1]) in parent.get_children():
            continue
        child = parent.add_child(Node(move_right(parent.data, data[0][e + 1]), parent))
        if check_failure(child.data):
            gwcgenerator(child.parent)
        if len(child.data.split('|')[1]) == 4:
            found.append(child)
            gwcgenerator(parent)
            continue
        child_data = child.data.split('|')
        for i in range(len(child_data[1])):
            if move_left(child.data, child_data[1][i]) in child.get_children():
                continue
            child1 = child.add_child(Node(move_left(child.data, child_data[1][i]), child))
            if not check_failure(child1.data):
                gwcgenerator(child1)
            if check_failure(child1.data):
                gwcgenerator(child1.parent)
    return found

def print_path(node):
    if node.parent == None:
        print(node.data)
        return True
    print(node.data)
    print_path(node.parent)

def check_failure(string):
    death = ["WG", "GC", "GW", "CG"]
    string = string.split('|')
    for e in death:
        if e == string[0]:
            return True
        if e == string[1]:
            return True
    return False

def move_right(whole_string, character):
    position = whole_string.find(character)
    whole_string = whole_string[:position] + whole_string[position + 1:] + character
    position = whole_string.find("F")
    whole_string = whole_string[:position] + whole_string[position + 1:] + "F"
    #print(whole_string)
    return whole_string


def move_left(whole_string, character):
    position = whole_string.find(character)
    whole_string = character+ whole_string[:position] + whole_string[position + 1:]
    position = whole_string.find("F")
    whole_string = "F" + whole_string[:position] + whole_string[position + 1:]
    #print(whole_string)
    return whole_string


if __name__ == "__main__":
    found = gwcgenerator(Node('FWCG|'))
    for e in found:
        print_path(e)