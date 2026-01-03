import os
import json

# Dossiers correspondant aux pages HTML
pages = {
    "portfolio": "images_portfolio",
    "projets": "images_projets"
}

all_categories = {}

for page, base_dir in pages.items():
    categories = {}
    if not os.path.exists(base_dir):
        print(f"⚠️ Dossier {base_dir} inexistant, page {page} ignorée")
        continue

    # On parcourt tous les sous-répertoires (1 niveau de profondeur)
    for root, dirs, files in os.walk(base_dir):
        # On ignore le dossier de base lui-même, on prend juste les sous-dossiers
        if root == base_dir:
            for folder in dirs:
                folder_path = os.path.join(base_dir, folder)
                image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

                if image_files:  # seulement si le dossier contient des images
                    categories[folder.lower()] = {
                        "title": folder,
                        "dir": f"{base_dir}/{folder}/",
                        "files": image_files,
                        "names": [os.path.splitext(f)[0] for f in image_files],
                        "desc": [f"Illustration du projet {os.path.splitext(f)[0]}" for f in image_files]
                    }

    all_categories[page] = categories

# Génère le fichier JS
with open("categories.js", "w", encoding="utf-8") as f:
    f.write("const allCategories = ")
    json.dump(all_categories, f, indent=2, ensure_ascii=False)
    f.write(";")

print("✅ categories.js généré avec les sous-répertoires pour toutes les pages !")
