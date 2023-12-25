# PIL
from PIL import Image
import glob, os


# Rotate image!
# CODE 
# with Image.open('./images/id_card.jpeg') as img:
#     img.rotate(45)
    
# Create Thumbnails
sizes = 128, 128
images = []

# To store thumbnails in  seprate folder
thumbnails_folder =  'thumbnails'
os.makedirs(thumbnails_folder, exist_ok=True)

for currFile in glob.glob('./images/*.jpeg'):
    file,ext =  os.path.splitext(os.path.basename(currFile))
    print(file, ext)

    
    with Image.open(currFile) as img:
    #    Convert to thumbnail size
        img.thumbnail(sizes)

        print(currFile)
        # extract file name only
        # ./images/WhatsApp.jpeg
       
        # Thumbnail Path
        thumbnail_path = os.path.join(thumbnails_folder, 
        file+'_thumb'+ext)
        img.save(thumbnail_path)

'''
Journal :
25.12.2023

While doing ohsint and exiftool python script I   Learnt what is PIL.
Used some methods like rotate, change image size to thumbnail size or other size.
'''
