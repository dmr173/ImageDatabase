from PIL import Image
import imagehash
import argparse
import shelve
import glob

types = ('*.jpg', '*.jpeg', '*.gif', '*.png', '*.bmp')
counter = 0

# open shelve database
db = shelve.open('db', writeback = True)

# Delete all values in db
for key in db.keys():
    del db[key]
print('db deleted, start loop with glob')

# loop over the images
for imagePath in glob.glob('w:/**/*.jpg', recursive=True):
    # load the image and compute hash
    image = Image.open(imagePath)
    h = str(imagehash.dhash(image))
    # update database
    filename = imagePath[imagePath.rfind("/") + 1:]
    db.get(h, []) + [filename]
    print(imagePath,': ',h)
# Limit processing to 100 files for testing
    counter += 1
    if counter > 100:
        break
# Print db content for testing
for key in db.keys():
    print(key,len(db[key]))

# close the shelve database
db.close()