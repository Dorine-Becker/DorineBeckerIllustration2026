import json
import os

# Extensions d'images à rechercher
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

# Chemins des fichiers
COMMENTAIRES_PATH = "commentaires.json"
OUTPUT_PATH = "categories.js"
TITLE_FILE = "Amelio_Affichage.txt"

# Répertoires sources → clés dans allCategories
SECTIONS = {
    "portfolio": "images_portfolio",
    "projets":   "images_projets",
}

# Répertoires à exclure du rendu public
EXCLUDED_DIRS = {"images_accueil"}


def read_title(dirpath, dir_name):
    """Lit le titre depuis Amelio_Affichage.txt, ou génère un fallback."""
    title_path = os.path.join(dirpath, TITLE_FILE)
    if os.path.exists(title_path):
        with open(title_path, "r", encoding="utf-8") as f:
            title = f.read().strip()
        if title:
            return title
    # Fallback : underscores -> espaces, première lettre en majuscule
    return dir_name.replace("_", " ").capitalize()


def find_images_in_section(section_dir, commentaires):
    """
    Parcourt les sous-répertoires d'un répertoire de section
    et retourne un dict { clé: données } trié alphabétiquement.
    """
    categories = {}

    if not os.path.isdir(section_dir):
        print(f"  Avertissement : répertoire '{section_dir}' introuvable, section ignorée.")
        return categories

    for dir_name in sorted(os.listdir(section_dir)):
        dirpath = os.path.join(section_dir, dir_name)
        if not os.path.isdir(dirpath):
            continue

        key = dir_name.lower()

        if key in EXCLUDED_DIRS:
            print(f"  Exclu : {dir_name}")
            continue

        images = sorted([
            f for f in os.listdir(dirpath)
            if f.lower().endswith(IMAGE_EXTENSIONS)
        ])

        if not images:
            print(f"  Ignoré (aucune image) : {dir_name}")
            continue

        title = read_title(dirpath, dir_name)
        dir_path = f"{section_dir}/{dir_name}/"
        vignette = images[0]

        content = []
        for filename in images:
            content.append({
                "file": filename,
                "text": commentaires.get(filename, ""),
            })

        categories[key] = {
            "title":    title,
            "dir":      dir_path,
            "vignette": vignette,
            "content":  content,
        }

    return categories


def format_js_value(value):
    return json.dumps(value, ensure_ascii=False)


def main():
    # Charger les commentaires
    if not os.path.exists(COMMENTAIRES_PATH):
        print(f"Erreur : fichier '{COMMENTAIRES_PATH}' introuvable.")
        return

    with open(COMMENTAIRES_PATH, "r", encoding="utf-8") as f:
        commentaires = json.load(f)

    lines = ["const allCategories = {"]
    section_keys = list(SECTIONS.keys())

    for s_idx, (section_key, section_dir) in enumerate(SECTIONS.items()):
        print(f"\nSection '{section_key}' ({section_dir}) :")
        cats = find_images_in_section(section_dir, commentaires)

        lines.append(f"  {format_js_value(section_key)}: {{")
        cat_keys = list(cats.keys())

        for c_idx, key in enumerate(cat_keys):
            cat = cats[key]
            is_last_cat = c_idx == len(cat_keys) - 1

            lines.append(f"    {format_js_value(key)}: {{")
            lines.append(f"      \"title\": {format_js_value(cat['title'])},")
            lines.append(f"      \"dir\": {format_js_value(cat['dir'])},")
            lines.append(f"      \"vignette\": {format_js_value(cat['vignette'])},")
            lines.append(f"      \"content\": [")

            for i, item in enumerate(cat["content"]):
                comma = "" if i == len(cat["content"]) - 1 else ","
                lines.append(
                    f"        {{ \"file\": {format_js_value(item['file'])}, "
                    f"\"text\": {format_js_value(item['text'])} }}{comma}"
                )

            lines.append(f"      ]")
            lines.append(f"    }}{',' if not is_last_cat else ''}")

            title_src = "Amelio_Affichage.txt" if os.path.exists(
                os.path.join(section_dir, key, TITLE_FILE)
            ) else "fallback"
            print(f"  {key!r} → \"{cat['title']}\" ({title_src}, {len(cat['content'])} image(s))")

        is_last_section = s_idx == len(section_keys) - 1
        lines.append(f"  }}{',' if not is_last_section else ''}")

    lines.append("};")

    output = "\n".join(lines)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\n'{OUTPUT_PATH}' généré avec succès.")


if __name__ == "__main__":
    main()
