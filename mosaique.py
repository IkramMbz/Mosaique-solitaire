import glob
import os
import random
from PIL import Image
from scipy import spatial
import numpy as np

# Gestion des tuiles
def initTiles(width, height):
    tile_paths = []

    for file in glob.glob("tiles/*"):
        tile_paths.append(file)

    tiles = []
    for path in tile_paths:
        tile = Image.open(path)
        tile = tile.resize((width, height))
        tiles.append(tile)

    # Calcule de la couleur dominante.
    colors = []
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

    return colors

def initPicture(main_photo_path):
    tilesWidth = tilesHeight = 5

    # Redimensionnement de notre image d'entrée.
    main_photo = Image.open(main_photo_path)
    width = int(np.round(main_photo.size[0] / tilesWidth))
    height = int(np.round(main_photo.size[1] / tilesHeight))
    resized_photo = main_photo.resize((width, height))  

    # Recherche de la tuile la plus proche pour chaque pixel.
    tree = spatial.KDTree(initTiles(tilesWidth,tilesHeight))

    # Recherche de la tuile la plus proche pour chaque pixel.
    closest_tiles = np.zeros((width, height), dtype=np.uint32)
    for i in range(width):
        for j in range(height):
            pixel = resized_photo.getpixel((i, j))
            closest = tree.query(pixel)
            closest_tiles[i, j] = closest[1]

    # Création de l'image de sortie.
    output = Image.new('RGB', main_photo.size)
    for i in range(width):
        for j in range(height):
            x, y = i*tile_size[0], j*tile_size[1]
            index = closest_tiles[i, j]
            output.paste(tiles[index], (x, y))

    filename = "output.jpg"
    name = 0
    while os.path.exists(filename):
        name += 1
        filename = f"output{name}.jpg"

    output.save(filename)

try:
    image_path = input("Saisissez le chemin d'accès à l'image : ")
    image = Image.open(image_path)
    initPicture(image_path)

except IOError:
    print("L'image n'a pas pu être ouverte. Veuillez vérifier que le chemin soit correct que le format est pris en charge.")