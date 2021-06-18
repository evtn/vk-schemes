from json import load


with open("build/schemes.json") as file:
    schemes = load(file)


def search(variables, parent, variable):
    """performs a recursive search of the variable"""

    value = variables.get(variable)

    if value:
        if value[0] == "$":
            return f"var(--{value[1:]})"
        return value

    if parent:
        parent = schemes[parent]
        variables = parent["variables"]
        parent = parent.get("parent")
        return search(variables, parent, variable)

    raise KeyError(f"Can't find '{variable}' variable anywhere, is it missing?")


def full_search(variables, parent):
    solved = {}
    undefined = {}

    while not solved or undefined:
        for name in schemes["default"]["variables"]:
            value = search(variables, parent, name)
            if value.startswith("@"):
                ref = value[1:]
                if ref in solved:
                    solved[name] = solved[ref]
                else:
                    undefined[name] = ref
            else:
                solved[name] = value
        for name in list(undefined):
            if undefined[name] in solved:
                solved[name] = solved[undefined[name]]
                undefined.pop(name)

    return solved
