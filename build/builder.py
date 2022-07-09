from utils import schemes, full_search
from config import version
from json import dump


def build_vars(variables):
    """builds variable definitions"""
    return "\n    ".join(f"--{name}: {variables[name]};" for name in sorted(variables))


def build(code):
    """builds a whole palette"""
    scheme = schemes[code]
    variables = full_search(scheme["variables"], scheme.get("parent"))

    return template.format(
        scheme_name=scheme["name"],
        scheme_code=code,
        branch=f"lord",
        variables=build_vars(variables),
        version=version,
    ), variables


with open("build/template.css") as file:
    template = file.read()


resolved_vars = {}


for code in schemes:
    if schemes[code].get("skip"):
        continue

    with open(f"styles/vk-{code}-scheme.user.css", "w") as file:
        print(f"building {code}")
        style, resolved_vars[code] = build(code)
        file.write(style)


with open("resolved_vars.json", "w") as file:
    dump(resolved_vars, file, ensure_ascii=False)