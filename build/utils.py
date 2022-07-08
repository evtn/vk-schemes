from init import schemes, default_palette


def search(variables, parent_key, variable):
    """performs a recursive search of the variable"""

    value = variables.get(variable)

    if value:
        if value[0] == "$":
            varname = value[1:]
            if varname in default_palette:
                return default_palette[varname]
            return f"var(--{varname})"
        if value[0] == "@":
            return value
        return value.upper()

    if parent_key:
        parent = resolve_parent(parent_key)
        variables = parent["variables"]
        return search(variables, parent.get("parent"), variable)

    raise KeyError(f"Can't find '{variable}' variable anywhere, is it missing?")


def resolve_parent(parent_key):
    if not parent_key:
        return parent_key

    if isinstance(parent_key, list):
        grandparents = []
        variables = {}
        for parent_subkey in parent_key:
            parent = resolve_parent(parent_subkey)

            grandparent = parent.get("parent", [])

            if isinstance(grandparent, list):
                grandparents.extend(grandparent)
            else:
                grandparents.append(grandparent)

            variables.update(parent["variables"])
        return {
            "parent": grandparents,
            "variables": variables,
        }

    return schemes[parent_key]


def gather_keys(variables, parent_key):
    if parent_key:
        parent_scheme = resolve_parent(parent_key)
        variables = parent_scheme["variables"]
        if isinstance(variables, str):
            variables = schemes[variables]["variables"]
        return set(variables) | gather_keys(variables, parent_scheme.get("parent"))
    return set(variables)


def full_search(variables, parent_key):
    solved = {}
    undefined = {}

    needed_keys = gather_keys(variables, parent_key)

    while not solved or undefined:
        for name in needed_keys:
            values = search(variables, parent_key, name).split(":")
            value = values[0]
            if value.startswith("@"):
                ref = value[1:]
                if ref in solved:
                    solved[name] = "".join([solved[ref], *values[1:]])
                else:
                    undefined[name] = ref, values[1:]
            else:
                solved[name] = value

        ref_count = len(undefined)

        for name in list(undefined):
            if undefined[name][0] in solved:
                ref, concat = undefined.pop(name)
                solved[name] = "".join([solved[ref], *concat])

        assert not ref_count or ref_count != len(undefined), f"Invalid palette, can't resolve:\n{undefined}"

    return solved
