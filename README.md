# Photo-Geo-Tagging
The project aims to update the metadata of the image files present in a directory by adding location and date information. This is achieved by mapping the file names to corresponding location and date information stored in a CSV file, and updating the image EXIF metadata with the corresponding values.

## Description
This project provides a set of functions to map Exif data to GPS coordinates and timestamps for images in a directory. The project includes the following functions:
- `create_exif_map()`: given a directory path and specified file extensions, extracts and aggregates Exif data for all image files in the directory into a CSV file.
- `map_images()`: given a directory path, loads all image files with specified file extensions, maps Exif data to GPS coordinates and timestamps using a CSV file as a reference, and writes new images with modified Exif data to a specified output directory. 

## Getting Started

### Dependencies

- Python 3.x
- Required packages: `pandas`, `Pillow`, `piexif`

### Installation

1. Clone the repo.
2. Install required packages with pip

## Usage
Explain how to use the project, including any relevant commands or arguments that need to be used. Provide examples of how to use the map_images and create_exif_map functions.

#### create_exif_map function
```python
def create_exif_map(df, 
                    location_column, 
                    datetime_column, 
                    lat_column = 'lat', 
                    long_column = 'long'):
    """
    Creates a dictionary mapping location and date information to the format required for EXIF metadata.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing the location and date information.
        location_column (str): Name of the column containing the location data.
        datetime_column (str): Name of the column containing the date data.
        lat_column (str, optional): Name of the column containing the latitude data. Defaults to 'lat'.
        long_column (str, optional): Name of the column containing the longitude data. Defaults to 'long'.

    Returns:
        dict: Dictionary containing the mapping data.
    """
    ```


#### map_images function
```python
def map_images(path,
               output_image_path,
               name_filters_l : list = ['.jpg', '.jpeg'],
               location_mapping_csv = "location_mapping.csv",
              ):
    """
    Maps location information from a CSV file to the EXIF metadata of images in a folder.

    Args:
        path (str): Path to the folder containing the images.
        output_image_path (str): Path to the output folder where the modified images will be saved.
        name_filters_l (list, optional): List of image file extensions to include. Defaults to ['.jpg', '.jpeg'].
        location_mapping_csv (str, optional): Path to the CSV file containing the location mapping data. Defaults to "location_mapping.csv".

    Returns:
        None
    """
```

## Examples
### Example 1: Creating an EXIF map
```python
from map_images import create_exif_map

directory_path = 'path/to/images'
exif_map = create_exif_map(directory_path=directory_path)
print(exif_map)
```
In this example, we use the create_exif_map function to create a dictionary mapping each image file name in the path/to/images directory to its EXIF data. We print out the resulting dictionary using the print function. This exif map will be used in the next function `map_images` to assign location tags to images without them based on the timestamps.

### Example 2: Mapping images
```python
from map_images import map_images

path = 'path/to/images'
output_image_path = 'path/to/output/images'
name_filters_l = ['.jpg', '.jpeg']
location_mapping_csv = 'path/to/location/mapping.csv'

map_images(path=path, output_image_path=output_image_path, name_filters_l=name_filters_l, location_mapping_csv=location_mapping_csv)
```
In this example, we use the map_images function to map location and time metadata to all images in the path/to/images directory. We save the mapped images to the path/to/output/images directory, and we filter images by the file extensions .jpg and .jpeg. We also specify the path to the location mapping CSV file, which is located at path/to/location/mapping.csv.


## Contributing
Contributions to this project are welcome. To contribute, please follow these steps:
* Fork the repository
* Create a new branch (git checkout -b feature/your-feature-name)
