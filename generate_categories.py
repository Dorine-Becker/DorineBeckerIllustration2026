import os
import json

# --- Configuration ---
pages = {
    "portfolio": "images_portfolio",
    "projets": "images_projets"
}

COMMENTS_FILE = "commentaires.json"
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

# --- Chargement des commentaires ---
def load_comments(path):
    if not os.path.exists(path):
        print("ℹ️ Aucun fichier de commentaires trouvé")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

comments = load_comments(COMMENTS_FILE)

all_categories = {}

# --- Parcours des pages ---
for page, base_dir in pages.items():
    categories = {}

    if not os.path.exists(base_dir):
        print(f"⚠️ Dossier {base_dir} inexistant, page {page} ignorée")
        continue

    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)

        if not os.path.isdir(folder_path):
            continue

        image_files = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(IMAGE_EXTENSIONS)
        ])

        if not image_files:
            continue

        # Première image = vignette
        vignette = image_files[0]
        gallery_files = image_files[1:]

        categories[folder.lower()] = {
            "title": folder.replace("_", " "),
            "dir": f"{base_dir}/{folder}/",
            "vignette": f"{base_dir}/{folder}/{vignette}",
            "files": gallery_files,
            "names": [os.path.splitext(f)[0] for f in gallery_files],
            "desc": [comments.get(f, "") for f in gallery_files]
        }

    all_categories[page] = categories

# --- Génération du JS ---
with open("categories.js", "w", encoding="utf-8") as f:
    f.write("const allCategories = ")
    json.dump(all_categories, f, indent=2, ensure_ascii=False)
    f.write(";")

print("✅ categories.js généré avec commentaires externes")
