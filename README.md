# Photo-Geo-Tagging
The project aims to update the metadata of the image files present in a directory by adding location and date information. This is achieved by mapping the file names to corresponding location and date information stored in a CSV file, and updating the image EXIF metadata with the corresponding values.

The project first extracts location data `(lat, long)` using EXIF information stored in pictures from the camera roll, and aggregates this data based on location and time to create clusters of locations. This information is saved in a csv file that is then used to assign each of the untagged images (images without gps location data) to one (or none) of the clusters of locations, based on datetime. 
![image](https://user-images.githubusercontent.com/45178011/230798658-d8963113-7977-4327-84fa-140cbf696a5d.png)


# Identify similar images
Given a folder with images, this project also allows you to identify potentially similar from within the folder and to aggreagte them. 
This is done using `ImageEmbedder.py` (to create embeddings for each of the images) and  `EmbeddingRetriever.py` (used to retrieve similar embeddings using either cosine distance or an approximation). 
The functions also return a dataframe with details about similar pictures.

An example nb can be found in `notebooks/find_similar_pictures.ipynb`.

# ImageProcessor Class

The `ImageProcessor` class is a Python class designed to simplify common image processing tasks related to file handling, listing, and EXIF data manipulation. This class provides methods to perform the following tasks:

1. Extract filenames from full file paths.
2. List picture files in a folder with specified file extensions.
3. Extract datetime information from filenames based on a specified pattern.
4. Clone an image, update its EXIF data with a new datetime, and save it.

## Usage

To use the `ImageProcessor` class, follow these steps:

1. Import the class:

```python
   from image_processor import ImageProcessor
```

Create an instance of the ```ImageProcessor``` class
```python
processor = ImageProcessor()
```
2. Use the class methods to perform various image processing tasks.

## Methods
```get_filename_from_path(file_path: str) -> str```
Extracts the filename from a full file path.
Parameters:
- ```file_path``` (str): The full file path.
Returns:
- ```str```: The extracted filename.

```list_pic_files_in_folder(folder_path: str, filters: list = ['jpg', 'jpeg']) -> list```
Lists picture files with specified file extensions in a folder.
Parameters:
- ```folder_path``` (str): The path to the folder.
- ```filters``` (list): A list of file extensions to filter (default: ['jpg', 'jpeg']).
Returns:
- ```list```: A list of picture files in the folder.

```extract_datetime_from_title(filename: str, filter_extensions: list = None) -> datetime.datetime```
Extracts datetime information from a filename based on a specified pattern.
Parameters
- ```filename``` (str): The filename to extract datetime from.
- ```filter_extensions``` (list): A list of file extensions to filter (default: ['jpg', 'jpeg']).
Returns
- ```datetime.datetime``` or ```None```: The extracted datetime object, or ```None``` if not found.

```clone_and_save_with_exif(original_filename: str, output_filename: str, datetime_obj: datetime.datetime) -> None```
Clones an image, updates its EXIF data with a new datetime, and saves it.
Parameters:
- ```original_filename``` (str): The path to the original image.
- ```output_filename``` (str): The path to save the cloned image with modified EXIF data.
- ```datetime_obj``` (datetime.datetime): The new datetime object for EXIF data.Example

## Example
Here's an example of how to use the ```ImageProcessor```

```python
from image_processor import ImageProcessor

processor = ImageProcessor()

# Define folder paths and filters
folder_path = '/path/to/your/source_folder'
folder_path_exif = '/path/to/your/output_folder'
filters = ['jpg', 'jpeg']

# Process images with EXIF data
processor.process_images_with_exif(folder_path, folder_path_exif, filters)
```




# Photo-geo-tagger


## Description
This project provides a set of functions to map Exif data to GPS coordinates and timestamps for images in a directory. The project includes the following functions:
- `create_exif_map()`: given a directory path and specified file extensions, extracts and aggregates Exif data for all image files in the directory into a CSV file.
- `map_images()`: given a directory path, loads all image files with specified file extensions, maps Exif data to GPS coordinates and timestamps using a CSV file as a reference, and writes new images with modified Exif data to a specified output directory. 

## Dependencies

- Python 3.x
- Required packages: `pandas`, `Pillow`, `piexif`

## Usage
Explain how to use the project, including any relevant commands or arguments that need to be used. Provide examples of how to use the map_images and create_exif_map functions.

#### create_exif_map function
```python
create_exif_map(camera_roll_example_path, 
                min_gps_threshold_similar=3,
                min_seconds_threshold_similar=1800, 
                output_exif_map='location_mapping.csv',
                name_filters_l=['.jpg', '.jpeg'],
                copy_grouped_pics_path=None)
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
    - path : str
        the directory path containing images to be mapped
    - output_image_path : str
        the directory path where the mapped images will be saved
    - name_filters_l : list of str, optional 
        a list of filename extensions to filter by, defaults to ['.jpg', '.jpeg']
    - location_mapping_csv : str, optional 
        the path to a CSV file containing location mapping data, defaults to "location_mapping.csv"

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

