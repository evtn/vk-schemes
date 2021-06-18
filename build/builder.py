from utils import schemes, full_search
from config import version
from os import getenv


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
        branch=f"build-{getenv('GITHUB_REF')}",
        variables=build_vars(variables),
        version=version,
    )


with open("build/template.css") as file:
    template = file.read()


for code in schemes:
    with open(f"styles/vk-{code}-scheme.user.css", "w") as file:
        print(f"building {code}")
        style = build(code)
        file.write(style)
