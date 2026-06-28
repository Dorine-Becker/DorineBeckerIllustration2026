import json
import os

# Extensions d'images à rechercher
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

# Chemins des fichiers
ANCIENS_COMMENTAIRES_PATH = "anciens_commentaires.json"
COMMENTAIRES_OUTPUT_PATH = "commentaires.json"
ORPHELINS_OUTPUT_PATH = "commentaires_orphelins.json"


def find_images(root_dir="."):
    """Parcourt récursivement les sous-répertoires et retourne tous les fichiers image trouvés."""
    images = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(IMAGE_EXTENSIONS):
                images.append(filename)
    return images


def main():
    # Charger les anciens commentaires
    if not os.path.exists(ANCIENS_COMMENTAIRES_PATH):
        print(f"Erreur : fichier '{ANCIENS_COMMENTAIRES_PATH}' introuvable.")
        return

    with open(ANCIENS_COMMENTAIRES_PATH, "r", encoding="utf-8") as f:
        anciens = json.load(f)

    # Trouver toutes les images dans les sous-répertoires
    images_trouvees = find_images(".")
    print(f"{len(images_trouvees)} image(s) trouvée(s).")

    # Construire commentaires.json
    commentaires = {}
    for filename in sorted(images_trouvees):
        commentaires[filename] = anciens.get(filename, "")

    with open(COMMENTAIRES_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(commentaires, f, ensure_ascii=False, indent=2)
    print(f"'{COMMENTAIRES_OUTPUT_PATH}' créé avec {len(commentaires)} entrée(s).")

    # Construire commentaires_orphelins.json
    noms_trouves = set(images_trouvees)
    orphelins = {
        nom: texte
        for nom, texte in anciens.items()
        if nom not in noms_trouves
    }

    with open(ORPHELINS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(orphelins, f, ensure_ascii=False, indent=2)
    print(f"'{ORPHELINS_OUTPUT_PATH}' créé avec {len(orphelins)} entrée(s) orpheline(s).")


if __name__ == "__main__":
    main()