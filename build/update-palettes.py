import requests
import json 
from utils import schemes

base_url = "https://raw.githubusercontent.com/VKCOM/Appearance/master/main.valette/"
scheme_url = f"{base_url}/scheme.json"
palette_url = f"{base_url}/palette.json"
web_palette_url = f"{base_url}/palette_web.json"

def get_palettes():
    base_palette = requests.get(palette_url).json()
    web_palette = requests.get(web_palette_url).json()

    merged = {**base_palette, **web_palette}

    return {k: merged[k] for k in sorted(merged)}


def get_schemes():
    schemes_file = requests.get(scheme_url).json()

    for scheme_key in schemes_file:
        scheme = schemes_file[scheme_key]
        target_key = scheme["appearance"]
        colors = scheme["colors"]
        schemes[target_key]["variables"] = target_scheme = {}

        for variable in colors:
            print(variable, colors[variable])
            target_scheme[variable] = f"${colors[variable]['color_identifier']}"
            if 'alpha_multiplier' in colors[variable]:
                target_scheme[variable] = f"{target_scheme[variable]}_alpha{int(colors[variable]['alpha_multiplier'] * 100)}"

        schemes[target_key]["variables"] = {
            k: target_scheme[k]
            for k in sorted(target_scheme)
        }


default_palette = get_palettes()
get_schemes()

with open("build/default_palette.json", "w") as file:
    json.dump(default_palette, file, indent=4, ensure_ascii=False)

with open("build/schemes.json", "w") as file:
    json.dump(schemes, file, indent=4, ensure_ascii=False)
