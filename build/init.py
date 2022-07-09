# filename is right, it should'nt be __init__.py

from json import load, dump
from os import listdir


# build schemes.json from schemes/*.json

scheme_files = listdir("build/schemes")
schemes = {}
file_lens = {}
for filename in scheme_files:
    with open(f"build/schemes/{filename}") as file:
        data = load(file)
        max_len = max(
            map(
                lambda k: len(data[k].get("variables", {})),
                data
            )
        )
        for k in data:
            file_lens[k] = max_len

        schemes.update(data)

for scheme_key in list(schemes):
    scheme = schemes[scheme_key]
    if not scheme.get("skip"):
        new_key = f"{scheme_key}-inverted-buttons"
        schemes[new_key] = {
            "name": f"{scheme['name']} Alternate Buttons",
            "description": f"Вариант {scheme['name']} с инвертированными цветами кнопок (цвет текста и фона кнопки поменяны местами)",
            "variant_of": scheme_key,
            "parent": [scheme_key, "inverted-buttons"],
            "variables": {}
        }
        file_lens[new_key] = file_lens[scheme_key]

schemes = {
    k: schemes[k] 
    for k in sorted(
        schemes, 
        key=file_lens.get,
        reverse=True
    )
}

with open("build/schemes.json", "w") as file:
    dump(schemes, file, indent=4, ensure_ascii=False)



# build default palette
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

with open("build/default_palette.json") as file:
    default_palette = build_alpha(load(file))