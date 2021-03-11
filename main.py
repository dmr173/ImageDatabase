from PIL import Image
import imagehash
import shelve
import glob
import mariadb
import sys
from datetime import datetime

types = ('*.jpg', '*.jpeg', '*.gif', '*.png', '*.bmp')
counter = 0
limit = 2500000
divisor = 100

# open MariaDB database
try:
    conn = mariadb.connect(
        user="root",
        password="MariaDB10@",
        host="10.10.10.20",
        port=3307,
        database="filehash"
    )
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)

# Get Cursor
cur = conn.cursor()

# Delete all values in db
cur.execute("TRUNCATE TABLE files")
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Table files truncated')

print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Building file list')
file_list = glob.glob('w:/**/*.jpg', recursive=True)
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Filecount: ', str(len(file_list)),' Limit: ',str(limit))

# loop over the images
for imagePath in file_list:
    # Try to load the image and compute hash
    try:
        image = Image.open(imagePath)
        h = str(imagehash.dhash(image))
    except:
        h = str('Error Hash Creation')
    # update database
    filename = imagePath[imagePath.rfind("/") + 1:]
    try:
        cur.execute("INSERT INTO files (hash,filename,path, filetype) VALUES (?, ?, ?,?)",
                    (h, filename, ' ',' '))
    except:
        print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Error inserting hash for: ',filename)

    counter += 1
    if counter % divisor == 0:
        conn.commit()
        print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Processed & Commited: ', str(counter))
# Limit processing to x files for testing
    if counter >= limit:
        break
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Processed: ', str(counter))

# Print db content to check/test

#print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - DB content: ')
#cur.execute("SELECT hash,count(*) as anzahl FROM files group by hash")   # Where Clause: "SELECT a,b,c FROM tab WHERE a=?",(filter_value,))
#for (hash, anzahl) in cur:
#    print(f"Anzahl: {anzahl}, Hash: {hash}")

# commit changes and close the database
conn.commit()
conn.close()
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"),' - Completed')
