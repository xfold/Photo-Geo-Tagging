# Photo-Geo-Tagging
The project aims to update the metadata of the image files present in a directory by adding location and date information. This is achieved by mapping the file names to corresponding location and date information stored in a CSV file, and updating the image EXIF metadata with the corresponding values.

The project first extracts location data `(lat, long)` using EXIF information stored in pictures from the camera roll, and aggregates this data based on location and time to create clusters of locations. This information is saved in a csv file that is then used to assign each of the untagged images (images without gps location data) to one (or none) of the clusters of locations, based on datetime. 
![image](https://user-images.githubusercontent.com/45178011/230798658-d8963113-7977-4327-84fa-140cbf696a5d.png)



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
    This function takes a path to a directory containing image files and creates a CSV file with mapping information based on the GPS coordinates of the images. It also groups images that were taken in the same location within a certain time frame.

    Parameters:
    -----------
    path : str
        Path to the directory containing image files
    min_gps_threshold_similar : float
        Maximum distance threshold in kilometers to consider two pictures taken at the same place
    min_seconds_threshold_similar : float
        Maximum time threshold in seconds to consider two pictures taken at the same place
    output_exif_map : str, optional (default: 'location_map.csv')
        Path to output CSV file with mapping information
    name_filters_l : List[str], optional (default: ['.jpg'])
        List of file extensions to consider when loading image files
    copy_grouped_pics_path : str, optional (default: None)
        Path to directory where grouped images should be saved as copies. If None, no copies are made.

    Returns:
    --------
    df : Dataframe
        df with with mapping information
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
    Maps GPS location and date metadata to images in a given directory.

    Parameters:
    -----------
    - path (str): the directory path containing images to be mapped
    - output_image_path (str): the directory path where the mapped images will be saved
    - name_filters_l (list of str, optional): a list of filename extensions to filter by, defaults to ['.jpg', '.jpeg']
    - location_mapping_csv (str, optional): the path to a CSV file containing location mapping data, defaults to "location_mapping.csv"

    Returns: 
    -----------
    None

    This function iterates over all image files in the given directory, and maps GPS location and date metadata to each image
    using data from the location_mapping_csv file. The modified images are saved in the specified output directory.

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
