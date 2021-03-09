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
#for key in db.keys():
#    del db[key]
#print('db deleted, start loop with glob')

# loop over the images
for imagePath in glob.glob('w:/Christel/**/*.jpg', recursive=True):
    # load the image and compute hash
    image = Image.open(imagePath)
    h = str(imagehash.dhash(image))
    # update database
    filename = imagePath[imagePath.rfind("/") + 1:]
    if h in db.keys():
       if not(filename in db[h]):
          db[h] =  db.get(h, []) + [filename]
    else:
        db[h] = [filename]
# Limit processing to x files for testing
    counter += 1
    if counter >= 2500:
        break

# Print db content to check/test
print('DB content: ',len(db.keys()),' different hash values')
for key in db.keys():
    if len(db[key])>1:
       print('Hash: ',key,': ',len(db[key]),' image(s) found: ',db[key])

# close the shelve database
db.close()