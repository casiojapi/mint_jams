import os
import json

TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{collection_name}</title>
    <link rel=\"stylesheet\" href=\"../../styles.css\">
</head>
<body>
    <header>
        <span class=\"brand\">mint_jams</span>
        <nav class=\"collections\">
            {collections_links}
        </nav>
        <span class=\"collection-name\">{collection_name}</span>
    </header>
    <main>
        <section class=\"gallery\">
            {images}
        </section>
    </main>
</body>
</html>"""

def load_collections():
    with open("collections.json", "r") as f:
        return json.load(f)

def generate_html():
    collections = load_collections()
    
    all_links = "".join(
        f'<a href="{name}.html" class="{"selected" if data["public"] else ""}">[[ {name} ]]</a>'
        for name, data in collections.items() if data["public"]
    )

    for name, data in collections.items():
        if not data["public"]:
            continue

        image_tags = "".join(
            f'<img src="../../{data["folderpath"]}/{img}" alt="{img}"><p>{img}</p>'
            for img in sorted(os.listdir(data["folderpath"]))[:data.get("up_to", 20)]
        )

        html_content = TEMPLATE.format(
            collection_name=name,
            collections_links=all_links,
            images=image_tags
        )

        with open(f"output/{name}.html", "w") as f:
            f.write(html_content)
    
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    generate_html()
    print("Collection pages generated successfully.")

