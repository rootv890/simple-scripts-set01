# Exif Tool Script
# Ref : David Bombal

#!/usr/bin/env python3
import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
import logo

# Helper Function to extract co-ordinates
def create_google_maps_url(gps_coords):
    #Exif tool stores co-ordinates into degree/minutes/seconds format to convert into decimal degrees.
    # 1. Extract the data from the dictionary we sent to this function for latitudinal data.
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
    # 2. Extract the data from the dictionary we sent to this function for longitudinal data.
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    # 3. Return a search string which can used in Google Maps
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"

# Function to convert degree/minutes/seconds to decimal degrees
def convert_decimal_degrees(degree, minutes,seconds, direction):
    decimal_degrees = degree +  minutes /60 + seconds/3600
    # Value of "S" for south or "W" for West will be multipled by -1
    if direction =='S' or direction =='W':
        decimal_degrees *= -1
    return decimal_degrees


# SKILLS SWAPPERS LOGO
logo.print_logo()
logo.print_tool()

# Giving a options wether output be in terminal or in .txt file
# if 1 -- In Terminal itself
# if 2 -- In text file
# if other loop the prompt

while True:
    output_choice = input('> How do you want to get the output:\n\n[1]: Terminal\n[2]: File\nEnter the choice here: ')
    # convert value to int
    try:
        conv_val = int(output_choice)
        if conv_val == 2:
            # Redirect the output to a file 
            fn = input('>Enter file name to save (leave blank if you want default name): ')
            if len(fn) < 1 :
                print ('DONE')
                sys.stdout = open('exif_data.txt', 'w')
                    
            else :
                print ('DONE')  
                sys.stdout = open(fn+'.txt', 'w')
                  
            break
            
        elif conv_val ==1:
            break
        else:
            print('You entered incorrect opton, please try again!.')
    except:
        print('You entered an invalid option, please try again!.')

# Add images to the folder ./images

# Assign os.getcwd to a variable(cwd) to get the path to images

cwd = os.getcwd() #cwd= current workind directory
# print(cwd)

#Change working directory to where images are i.e, by joining ./images to cwd
os.chdir(os.path.join(cwd,'images'))
# Get list of all the files(images) in the images dir
files = os.listdir()

# CHeck if there are any files in the ./images dir

if len(files) == 0:
    print("You don't have any images in the ./images folder!")
    exit()

for file in files:
    # Using Try/except block to handle where there are wrong file formats in ./images folder.
    try:
        pass
        # Open the image file using Image of PIL. Open the file in binary format for reading
        with Image.open(file) as img:
            print(f"\n-----[Image Name : {file}]-----")
            
            # print(img)
            gps_coords = {}
            # Check if image has any exit data or not
            if img._getexif() == None:
                print(f"{file} has no exif data!")
            # If at all exif data exits Loop/cycle through the tag and value for the file.
            else :
                for tag,value in img._getexif().items():
                    tag_name = TAGS.get(tag)
                    
                    if tag_name == 'GPSInfo':
                        for key, val  in value.items():
                            # print the gps data value for every ket to the screen
                            print(f"{GPSTAGS.get(key)}- {val}")
                            # We add Latitude data to the gps_coord dictionary which we initialized in line 110.
                            if GPSTAGS.get(key) == 'GPSLatitude':
                                gps_coords['lat'] = val
                            # We add Longitude data to the gps_coord dictionary which we initialized in line 110.
                            elif GPSTAGS.get(key) == "GPSLongitude":
                                gps_coords["lon"] = val
                            elif GPSTAGS.get(key) == "GPSLatitudeRef":
                                gps_coords["lat_ref"] = val
                            # We add Longitude reference data to the gps_coord dictionary which we initialized in line 110.
                            elif GPSTAGS.get(key) == "GPSLongitudeRef":
                                gps_coords["lon_ref"] = val 
                    else :
                      print(f"{tag_name} - {value}") 
                # Print the long. and lat data which has been formatted for Google Maps. It is did only to so if the GPS cordinate exis.
                if gps_coords:
                    # TODO : 
                    print(create_google_maps_url(gps_coords))     
                # Change back to the orginal wokring director
         
    except IOError:
        print('File Format not supprted')

print('DONE')      

if output_choice == '2':  # Output in File
    
    sys.stdout.close()

os.chdir(cwd)
