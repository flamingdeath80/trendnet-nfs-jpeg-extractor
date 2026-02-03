# Trendnet NFS JPEG Extractor

A Python utility to extract JPEG images from Trendnet IP camera NFS storage files, bypassing the need for proprietary software.

## Overview

Trendnet IP cameras (specifically model **TV-IP327PI** and potentially other models) save triggered event images to network storage in a proprietary format. When configured to use NFS storage for motion detection or line-crossing events, the camera creates `.pic` (BIN) files containing embedded JPEG and JSON data. This format requires Trendnet's proprietary software to access the images.

This script solves that problem by extracting the JPEG images directly from these `.pic` files and saving them as standard `.jpg` files, organized by date.

## Features

- **Extracts embedded JPEG images** from Trendnet `.pic` files
- **Automatic date-based organisation** - Creates folders named with current date (YYYY-MM-DD)
- **Sequential numbering** - Names extracted images as `image_0000.jpg`, `image_0001.jpg`, etc.
- **Cleanup after extraction** - Removes JPEG data from source files after extraction
- **Automatic ownership management** - Sets proper file ownership (configurable)
- **Batch processing** - Processes all `.pic` files in the input directory

## Supported Cameras

- **Trendnet TV-IP327PI** (confirmed)
- Other Trendnet IP camera models that use similar NFS storage formatting (unconfirmed)

## Requirements

- Python 3.x
- Read/write access to the NFS mount point
- Appropriate permissions to change file ownership (if using the ownership features)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/flamingdeath80/trendnet-nfs-jpeg-extractor.git
cd trendnet-nfs-jpeg-extractor
```

2. Ensure your NFS share is mounted (example):
```bash
sudo mount -t nfs camera_ip:/share /srv/nfs/camera
```

## Configuration

Before running the script, edit the following variables in `Trendnet-jpg-nfs-extraction.py`:

```python
# Input folder containing .pic files from your Trendnet camera
input_folder = "/srv/nfs/camera/datadir0/"

# Output folder where JPEGs will be saved
base_output_folder = "/home/me/jpg1/"
```

If you want to modify file ownership, adjust these lines (or comment them out if not needed):
```python
shutil.chown(output_folder, user="me", group="me")
shutil.chown(image_path, user="me", group="me")
```

## Usage

Run the script:
```bash
python3 Trendnet-jpg-nfs-extraction.py
```

### What Happens:

1. The script scans the input folder for `.pic` files
2. Searches for JPEG markers (`0xFFD8` start, `0xFFD9` end) within each file
3. Extracts each JPEG image found
4. Saves images to a date-stamped folder: `/home/me/jpg1/2026-01-20/`
5. Images are named sequentially: `image_0000.jpg`, `image_0001.jpg`, etc.
6. Removes the extracted JPEG data from the original `.pic` files

### Example Output:

```
Extracted 5 images from 'file001.pic' into folder '/home/me/jpg1/2026-01-20' and removed their data from '/srv/nfs/camera/datadir0/file001.pic'.
Extracted 3 images from 'file002.pic' into folder '/home/me/jpg1/2026-01-20' and removed their data from '/srv/nfs/camera/datadir0/file002.pic'.
No JPEG images found in the file 'file003.pic'.
```

## Automation

To run this script automatically (e.g., every 5 minutes), add a cron job:

```bash
crontab -e
```

Add the line:
```
*/5 * * * * /usr/bin/python3 /path/to/Trendnet-jpg-nfs-extraction.py >> /var/log/trendnet-extraction.log 2>&1
```

## How It Works

The script uses byte-level file operations to:

1. **Detect JPEG boundaries** using standard JPEG markers:
   - Start: `0xFFD8`
   - End: `0xFFD9`

2. **Extract image data** between these markers

3. **Preserve non-JPEG data** (like JSON metadata) by writing it back to the original file

4. **Handle multiple JPEGs** within a single `.pic` file

## Limitations

- **JSON metadata is not extracted** - The script currently only extracts JPEG images, not the accompanying JSON metadata that may be present in the `.pic` files
- **Destructive operation** - The original `.pic` files are modified (JPEG data removed). Keep backups if needed.
- **No error recovery** - If the script crashes mid-extraction, files may be in an inconsistent state

## Troubleshooting

### Permission Denied Errors
Ensure you have read/write permissions on both the input and output folders:
```bash
sudo chown -R yourusername:yourgroup /srv/nfs/camera
chmod -R 755 /home/me/jpg1
```

### No Images Extracted
- Verify the `.pic` files actually contain JPEG data
- Check that the input folder path is correct
- Ensure the camera is configured for single-frame image capture (not video)

### Ownership Issues
If you don't need to change file ownership, comment out these lines:
```python
# shutil.chown(output_folder, user="me", group="me")
# shutil.chown(image_path, user="me", group="me")
```

## Contributing

Contributions are welcome! If you have:
- Tested this with other Trendnet camera models
- Improvements to the extraction algorithm
- Ideas for JSON metadata extraction
- Bug fixes or enhancements

Please open an issue or submit a pull request.

## License

This project is provided as-is under the MIT License. See [LICENSE](LICENSE) file for details.

## Acknowledgments

Created to solve the proprietary format limitation of Trendnet IP cameras and enable open-source access to triggered event images.

## Disclaimer

This software is not affiliated with or endorsed by Trendnet. Use at your own risk. Always maintain backups of important data.

---

**Found this helpful?** Star this repository to help others discover it!
