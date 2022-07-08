from json import load
from os.path import exists


part_template = """
<li>
    <details>
        <summary><b>{name}</b>: {description}</summary>

    {image}
    [![{name}]({badge})](https://github.com/evtn/vk-schemes/raw/build-stable/vk-{code}-scheme.user.css)

    {variants_text}

    </details>
</li>
"""


variants_template = """Варианты:

<ul>
    {0}
</ul>
"""


image_template = "![{name} Screenshot](images/{code}.png)"
badge_template = "https://img.shields.io/static/v1?label={badge_name}&message=%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C&style=for-the-badge&labelColor={background_content}&color={accent}"


with open("build/schemes.json") as file:
    schemes = load(file)

with open("resolved_vars.json") as file:
    resolved_vars = load(file)


rendered_schemes = []
variants = {}



def render_scheme(scheme_key, tab_level=0):
    print("render:", " " * (tab_level * 4 - 1), scheme_key)

    tab = tab_level * 4 * " "

    scheme = schemes[scheme_key]
    image = ""
    badge = badge_template.format(
        badge_name=scheme["name"].replace(" ", "%20"),
        accent=resolved_vars[scheme_key]["accent"].replace("#", ""),
        background_content=resolved_vars[scheme_key]["background_content"].replace("#", "")
    )

    if exists(f"images/{scheme_key}.png"):
        image = image_template.format(**scheme)

    variants_text = ""

    if scheme_key in variants:
        variants_text = variants_template.format(
            "\n\n".join([
                render_scheme(variant, tab_level + 1)
                for variant in variants[scheme_key]
            ])
        )

    scheme_part = part_template.format(
        image=image,
        badge=badge,
        variants_text=variants_text,
        **scheme,
    )

    return (scheme_part).replace("\n", "\n" + tab)



for scheme_key in schemes:
    scheme = schemes[scheme_key]
    scheme["code"] = scheme_key
    if scheme.get("skip"): # skipped schemes
        continue
    if (base := scheme.get("variant_of")):
        variants[base] = variants.get(base, [])
        variants[base].append(scheme_key)


for scheme_key in schemes:
    scheme = schemes[scheme_key]
    if scheme.get("skip"): # skipped schemes
        continue

    if scheme.get("variant_of"):
        continue

    rendered_schemes.append(render_scheme(scheme_key))


with open("readme_template.md") as file:
    readme_template = file.read()

with open("readme.md", "w") as file:
    file.write(
        readme_template.format(
            schemes="\n\n".join(rendered_schemes),
        )
    )

