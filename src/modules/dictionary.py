from typing import Optional
import graphviz


class Node:
    def __init__(
        self,
        value: str,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        index: Optional[int] = None,
    ):
        self.value = value
        self.left = left
        self.right = right
        self.index = index

    def __repr__(self):
        return f"Node({self.value})"


def convert_list_to_str(input_list: list[str]) -> str:
    """
    asumption : array has been sorted
    Input: `['Abidin', 'Abilah', 'Abimana', 'Abing', 'Abiogenesis']`
    Output: `6Abidin6Abilah7Abimana5Abing11Abiogenesis`
    """
    result = ""
    for term in input_list:
        result += str(len(term)) + term
    return result


def parse_string_to_list(input_string: str) -> list[str]:
    """
    Input: `6Abidin6Abilah7Abimana5Abing11Abiogenesis`
    Output: `['Abidin', 'Abilah', 'Abimana', 'Abing', 'Abiogenesis']`
    """
    result = []
    i = 0
    while i < len(input_string):
        # get the number of characters to extract
        length_start = i
        while i < len(input_string) and input_string[i].isdigit():
            i += 1
        length = int(input_string[length_start:i])

        # extract string
        result.append(input_string[i : i + length])
        i += length
    return result


def _generate_node(
    root: Node,
    graph: graphviz.Graph,
    input: list[str],
    index_list: list[str],
    direction: Optional[str] = "left",
    skip: Optional[int] = 3,
):
    print(input)
    if len(input) == 0:
        return

    if len(input) < (skip + 1):
        if direction == "left":
            prev = root
            for term in input:
                node = Node(value=term, index=index_list.index(term))
                graph.node(term, label=term)

                prev.left = node
                graph.edge(prev.value, term, color="green")

                prev = node
        else:
            reversed_input = input[::-1]

            node = Node(value=reversed_input[0], index=index_list.index(input[0]))
            graph.node(node.value, label=node.value)

            root.right = node
            graph.edge(root.value, node.value, color="red")
            
            # the rest is always on left
            _generate_node(node, graph, reversed_input[1:], index_list)
    else:
        # left
        new_root_node = Node(value=input[skip], index=index_list.index(input[skip]))
        graph.node(new_root_node.value, label=new_root_node.value)

        if direction == "left":
            root.left = new_root_node
        elif direction == "right":
            root.right = new_root_node
        color = "green"
        if direction == "right":
            color="red"
        graph.edge(root.value, new_root_node.value, color=color)

        prev = new_root_node
        for i in range(skip):
            idx = skip - i - 1
            node = Node(value=input[idx], index=index_list.index(input[idx]))
            graph.node(node.value, label=node.value)

            prev.left = node
            graph.edge(prev.value, node.value, color="green")

            prev = node

        # right
        _generate_node(
            new_root_node, graph, input[skip + 1 :], index_list, direction="right"
        )


def generate_blocking_tree(
    input: list[str],
    index_list: list[str],
) -> tuple[Node, graphviz.Graph]:
    """
    Input: `['Abidin', 'Abilah', 'Abimana', 'Abing', 'Abiogenesis']`
    Output: The root node of the tree, graphviz.Graph object
    """
    if len(input) == 0:
        return None
    graph = graphviz.Graph(comment="Blocking Tree")
    sorted_input = sorted(input)

    mid = len(sorted_input) // 2
    value = sorted_input[mid]
    root = Node(value=value)
    graph.node(value, label=value)

    _generate_node(root, graph, sorted_input[:mid], index_list, "left")  # left
    _generate_node(root, graph, sorted_input[mid + 1 :], index_list, "right")  # right

    return root, graph


def _search_tree(term: str, tree: Optional[Node]):
    if tree is not None:
        print(f"->{tree}", end="")
        if term == tree.value:
            return tree
        elif term < tree.value:
            left_node = tree.left
            while left_node is not None:
                print(f"->{left_node}", end="")
                if term == left_node.value:
                    print()
                    return left_node
                else:
                    left_node = left_node.left
        elif term > tree.value:
            return _search_tree(term, tree.right)


def search_bloking_tree(
    term: str,
    tree: Node,
) -> Optional[Node]:
    if tree is None:
        return None

    print(f"{tree}", end="")

    if term == tree.value:
        return tree
    elif term < tree.value:
        return _search_tree(term, tree.left)
    elif term > tree.value:
        return _search_tree(term, tree.right)
    return None


string = "8Abiosfer7Abiotik4Abis6Abisal7Abiseka9Abiturien5Abjad8Abjadiah6Ablasi6Ablaut8Ablepsia5Ablur8Abnormal12Abnormalitas5Abnus4Aboi7Abolisi4Abon8Abonemen11Abong-abong6Aborsi7Abortif8Abortiva7Abortus5Abrak11Abrakadabra5Abrar5Abras6Abrasi8Abreaksi5Abrek9Abreviasi7Abrikos11Abrit-abrit8Abrosfer7Abrupsi5Absah5Absen7Absensi7Absente11Absenteisme5Abses5Absis8Absolusi7Absolut"
parse = parse_string_to_list(string)

root, graph = generate_blocking_tree(parse, sorted(parse))
result = search_bloking_tree("Abortif", root)

print("\n\nresult", result)
