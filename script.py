import re
import os
import json
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{collection_name}</title>
    <script>
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'j') {{
                window.scrollBy({{ top: 150, behavior: 'smooth' }});
            }} else if (event.key === 'k') {{
                window.scrollBy({{ top: -200, behavior: 'smooth' }});
            }}
        }});
    </script>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{
            background-color: {background_color};
        }}
        .gallery p {{
            color: {caption_color};
        }}
    </style>
</head>
<body>
    <header>
        <span class="brand">mint_jams</span>
        <nav class="collections">
            {collections_links}
        </nav>
        <span class="collection-name">"{collection_name}"</span>
    </header>
    <main>
        <section class="gallery">
            {images}
        </section>
    </main>
    <div class="help-text">use j ↓ k ↑ to move<br><br>go fullscreen: press F11</div>
</body>
</html>"""

# si, es javascript. pero es el unico que puede resolver este problema. Asi que si no te gusta enjoyear las gains de las vim motions usa tu JSBLOCKER mhmhmhmhmhmhmmmmmmmmmmmmmmm *ACTIVANDO JSBLOCKER* (un gordo cosplay de sailor moon gritando mientras activa su increible y vegano escudo con rubies (main taric)) AAAAAAKKKKKKKKKKKKKKKKKDDDDTTHCHHTTTUAAAALLLLYYYYYYYYYY podrias.... mHHMMMMmm... hacerlooo....>>>GNGNNGNG.....,.,, CLNP..,,..,IPX/SPXXXXXXXXXX..........


def sanitize_filename(name):
    """Convert collection name to a safe filename: lowercase, hyphens, no spaces or special chars."""
    return re.sub(r'[()\s~]+', '-', name.lower()).lstrip('-')

def load_collections():
    with open("collections.json", "r") as f:
        return json.load(f)

def generate_html():
    collections = load_collections()
    
    all_links = "".join(
        f'<a href="{sanitize_filename(name)}.html" class="{"selected" if data["public"] else ""}">[[ {name} ]]</a>'
        for name, data in collections.items() if data["public"]
    )

    for name, data in collections.items():
        if not data["public"]:
            continue

        # Determine background and caption colors based on 'dark' boolean
        is_dark = data.get("dark", True)  # Default to dark if not specified
        background_color = "#020005" if is_dark else "#FFFFFF"
        caption_color = "#FFFFFF" if is_dark else "#000000"

        image_tags = "".join(
            f'<img src="{data["folderpath"]}/{img}" alt="{img}"><p>{img}</p>'
            for img in sorted(os.listdir(data["folderpath"]))[:data.get("up_to", 20)]
        )

        html_content = TEMPLATE.format(
            collection_name=name,
            collections_links=all_links,
            images=image_tags,
            background_color=background_color,
            caption_color=caption_color
        )

        with open(f"{sanitize_filename(name)}.html", "w") as f:
            f.write(html_content)
    
if __name__ == "__main__":
    os.makedirs("./", exist_ok=True)
    generate_html()
    print("Collection pages generated successfully.")
