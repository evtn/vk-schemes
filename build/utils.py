from json import load


def get_alpha(color, alpha):
    return f"{color[:7]}{round(alpha / 100 * 255):02x}".upper()


def build_alpha(palette):
    new_palette = {}
    for key in palette:
        if len(palette[key]) == 9: # color format is ARGB for some reason, what the...
            palette[key] = f"#{palette[key][3:]}{palette[key][1:3]}"
        new_palette[key] = palette[key]
        if "alpha" in key:
            continue
        for alpha in range(0, 100, 4):
            new_palette[f"{key}_alpha{alpha}"] = get_alpha(palette[key], alpha)
    return new_palette


with open("build/schemes.json") as file:
    schemes = load(file)

with open("build/default_palette.json") as file:
    default_palette = build_alpha(load(file))

def search(variables, parent, variable):
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

    if parent:
        parent = schemes[parent]
        
        variables = parent["variables"]
        if isinstance(variables, str):
            variables = schemes[variables]["variables"]
        parent = parent.get("parent")
        return search(variables, parent, variable)

    raise KeyError(f"Can't find '{variable}' variable anywhere, is it missing?")


def gather_keys(variables, parent):
    if parent:
        parent_scheme = schemes[parent]
        variables = parent_scheme["variables"]
        if isinstance(variables, str):
            variables = schemes[variables]["variables"]
        return set(variables) | gather_keys(variables, parent_scheme.get("parent"))
    return set(variables)


def full_search(variables, parent):
    solved = {}
    undefined = {}

    needed_keys = gather_keys(variables, parent)

    while not solved or undefined:
        for name in needed_keys:
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

        ref_count = len(undefined)

        for name in list(undefined):
            if undefined[name][0] in solved:
                ref, concat = undefined.pop(name)
                solved[name] = "".join([solved[ref], *concat])

        assert not ref_count or ref_count != len(undefined), f"Invalid palette, can't resolve:\n{undefined}"

    return solved
