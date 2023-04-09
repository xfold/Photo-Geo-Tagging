# Photo-Geo-Tagging
The project aims to update the metadata of the image files present in a directory by adding location and date information. This is achieved by mapping the file names to corresponding location and date information stored in a CSV file, and updating the image EXIF metadata with the corresponding values.


### Usage
Explain how to use the project, including any relevant commands or arguments that need to be used. Provide examples of how to use the map_images and create_exif_map functions.

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
#### create_exif_map function
```python

python
Copy code
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
