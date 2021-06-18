from utils import schemes, full_search
from json import dump


def build_tree():
    tree = {}
    for code in schemes:
        if "parent" in schemes[code]:
            parent = schemes[code]["parent"]
            tree[parent] = tree.get(parent, [])
            tree[parent].append(code)
    return tree


def optimize_tree(tree, code):
    for child_code in tree[code]:
        print(f"Optimizing {child_code}")
        deleted = 0
        child = schemes[child_code]["variables"]
        solved_child = full_search(child, code)
        for name in list(child):
            subset = child.copy()
            subset.pop(name)
            if full_search(subset, code).get(name) == solved_child.get(name):
                child.pop(name)
                deleted += 1

        print(f"Deleted {deleted} extra keys")
        
        if child_code in tree:
            optimize_tree(tree, child_code)


tree = build_tree()
optimize_tree(tree, "default")

with open("build/schemes.json", "w") as file:
    dump(schemes, file, indent=4)
