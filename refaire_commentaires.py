"""
après avoir renommé commentaires.json en anciens_commentaires.json :
écrasement du fichier commentaires.json qui est un dictionnaire avec comme clés tous les noms de fichiers trouvés sur les répertoires d'images
(les répertoires dont le nom commence par 'images', récursivement)
et comme Values les commentaires qui existaient auparavant, pris dans anciens_commentaires.json si le nom correspond

les commentaires d'images qui n'existent plus sont récupérés dans

ce fichier doit être complété à la main pour éventuellement insérer des descriptions sur les images qui n'en ont pas"""

import os
import json

# --- Extensions acceptées ---
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

les_anciens = "anciens_commentaires.json"
les_nouveaux = "commentaires.json"
description_sans_image_correspondante = "commentaires_sans_images.json"

def charger_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def trouver_images():
    images = set()
    for root, dirs, files in os.walk("."):
        parts = root.split(os.sep)
        if not any(p.startswith("images") for p in parts):
            continue
        for f in files:
            if f.lower().endswith(IMAGE_EXTENSIONS):
                images.add(f)
    return images

def main():
    anciens = charger_json(les_anciens)
    images_trouvees = trouver_images()

    result = {}
    commentaires_sans_images = {}

    for img in images_trouvees:
        result[img] = anciens.get(img, "")

    # Trouver les commentaires sans images associées
    for fichier, commentaire in anciens.items():
        if fichier not in images_trouvees:
            commentaires_sans_images[fichier] = commentaire

    # --- TRI ALPHABÉTIQUE ICI ---
    result = dict(sorted(result.items(), key=lambda x: x[0].lower()))
    commentaires_sans_images = dict(sorted(commentaires_sans_images.items(), key=lambda x: x[0].lower()))

    # sauvegarde
    with open(les_nouveaux, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    with open(description_sans_image_correspondante, "w", encoding="utf-8") as f:
        json.dump(commentaires_sans_images, f, ensure_ascii=False, indent=2)

    print(f"{len(result)} images enregistrées dans {les_nouveaux} (triées)")
    print(f"{len(commentaires_sans_images)} commentaires sans images enregistrés dans {description_sans_image_correspondante}")

if __name__ == "__main__":
    main()