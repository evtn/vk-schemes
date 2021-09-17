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
            values = search(variables, parent, name).split(":")
            value = values[0]
            if value.startswith("@"):
                ref = value[1:]
                if ref in solved:
                    solved[name] = "".join([solved[ref], *values[1:]])
                else:
                    undefined[name] = ref, values[1:]
            else:
                solved[name] = value

        for name in list(undefined):
            if undefined[name][0] in solved:
                ref, concat = undefined.pop(name)
                solved[name] = "".join([solved[ref], *concat])

    return solved
