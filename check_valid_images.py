import imghdr
import os

images_dir = 'assets/images'
corrupted = []
for f in os.listdir(images_dir):
    path = os.path.join(images_dir, f)
    if os.path.isfile(path):
        if imghdr.what(path) is None:
            corrupted.append(f)

if corrupted:
    for c in corrupted:
        print(f"CORRUPTED OR NOT IMAGE: {c}")
else:
    print("ALL IMAGES VALID")
