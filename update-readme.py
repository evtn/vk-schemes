from json import load
from os.path import exists


part_template = """
<details>
    <summary><b>{name}</b>: {description}</summary>

{image}
[![Ayu]({badge})](https://github.com/evtn/vk-schemes/raw/build-stable/vk-{code}-scheme.user.css)

</details>
"""

image_template = "![{name} Screenshot](images/{code}.png)"
badge_template = "https://img.shields.io/static/v1?label={badge_name}&message=%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C&style=for-the-badge&labelColor={background_content}&color={accent}"


with open("build/schemes.json") as file:
    schemes = load(file)

with open("resolved_vars.json") as file:
    resolved_vars = load(file)


common_schemes = []
variants = []

for scheme_key in schemes:
    scheme = schemes[scheme_key]
    scheme["code"] = scheme_key
    print(scheme_key)
    if scheme_key not in resolved_vars: # skipped schemes
        continue

    image = ""
    badge = badge_template.format(
        badge_name=scheme["name"].replace(" ", "%20"),
        accent=resolved_vars[scheme_key]["accent"].replace("#", ""),
        background_content=resolved_vars[scheme_key]["background_content"].replace("#", "")
    )

    if exists(f"images/{scheme_key}.png"):
        image = image_template.format(**scheme)

    scheme_part = part_template.format(
        image=image,
        badge=badge,
        **scheme,
    )
    if scheme.get("is_variant"):
        variants.append(scheme_part)
    else:
        common_schemes.append(scheme_part)


with open("readme_template.md") as file:
    readme_template = file.read()

with open("readme.md", "w") as file:
    file.write(
        readme_template.format(
            common_schemes="\n\n".join(common_schemes),
            variants="\n\n".join(variants)
        )
    )

