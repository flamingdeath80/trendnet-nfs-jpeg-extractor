import os
from datetime import datetime
import shutil

# Define the input folder containing .pic files and the output base folder
input_folder = "/srv/nfs/camera/datadir0/"
base_output_folder = "/home/me/jpg1/"

# Capture today's date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")
output_folder = os.path.join(base_output_folder, current_date)

# Create the dated output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Change ownership of the dated output folder to user "me" and group "me"
shutil.chown(output_folder, user="me", group="me")

# Retrieve and sort the .pic files in correct numerical order
pic_files = sorted(
    [f for f in os.listdir(input_folder) if f.endswith(".pic")]
)

# JPEG markers
start_marker = b'\xff\xd8'  # JPEG start
end_marker = b'\xff\xd9'    # JPEG end

# Loop through the sorted .pic files
for pic_file in pic_files:
    input_file = os.path.join(input_folder, pic_file)

    # Read the .pic file
    with open(input_file, "rb") as infile:
        data = infile.read()

    # Initialize variables
    count = 0
    pos = 0
    found = False

    # Buffer to hold non-JPEG data
    remaining_data = bytearray()

    # Check for JPEG files and extract them
    while True:
        start = data.find(start_marker, pos)
        if start == -1:
            # Add any remaining data after the last JPEG
            remaining_data.extend(data[pos:])
            break
        end = data.find(end_marker, start) + 2
        if end == 1:
            # Add data to the buffer if no valid JPEG end marker is found
            remaining_data.extend(data[pos:])
            break
        found = True
        # Add non-JPEG data before the current JPEG to the buffer
        remaining_data.extend(data[pos:start])
        # Ensure unique filenames
        while os.path.exists(os.path.join(output_folder, f"image_{count:04d}.jpg")):
            count += 1
        image_path = os.path.join(output_folder, f"image_{count:04d}.jpg")
        with open(image_path, "wb") as outfile:
            outfile.write(data[start:end])
        # Change ownership of the file to user: "me" and group: "me"
        shutil.chown(image_path, user="me", group="me")
        count += 1
        pos = end

    # Overwrite the .pic file with remaining data (non-JPEG)
    with open(input_file, "wb") as outfile:
        outfile.write(remaining_data)

    # Output the result for the current file
    if found:
        print(f"Extracted {count} images from '{pic_file}' into folder '{output_folder}' and removed their data from '{input_file}'.")
    else:
        print(f"No JPEG images found in the file '{pic_file}'.")