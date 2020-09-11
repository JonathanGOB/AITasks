import copy


class Node:
    data = None
    parent = None
    children = []

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

    def add_children(self, child):
        self.children.append(child)


visited = set()

start_node = Node(({"F", "C", "G", "W"}, set()))


def generator(node):
    pass


def is_valid(node):
    for x in node.data:
        if "W" and "G" in x:
            if "F" in x:
                continue
            else:
                return False
        if "C" and "G" in x:
            if "F" in x:
                continue
            else:
                return False
    return True


print(is_valid(Node(({"F", "C", "G", "W"}, set()))))
print(is_valid(Node(({"C", "G", "W"}, {"F"}))))


def is_goal(node):
    if len(node.data[1]) == 4:
        print("goal")
        return True
    else:
        return False


def move_right(node, action):
    new_node = copy.deepcopy(node)
    for x in action:
        new_node.data[0].remove(x)
        new_node.data[1].add(x)
    return new_node


def move_left(node, action):
    new_node = copy.deepcopy(node)
    for x in action:
        new_node.data[1].remove(x)
        new_node.data[0].add(x)
    return new_node