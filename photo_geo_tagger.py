from exif import Image
import os
import math
from datetime import datetime, timedelta
import geopy.distance
from statistics import mean
import pandas as pd
import ast

from helpers import _load_images, _get_exifs, _is_closer_than_n_kms, _is_in_time, _save_copy_pics, _get_lat_long_decimal, _dd2dms, _get_image_modified_data, _map_location_mapping


def create_exif_map(path: str, 
                    min_gps_threshold_similar: float, 
                    min_seconds_threshold_similar: float, 
                    output_exif_map: str = 'location_map.csv',
                    name_filters_l : list = ['.jpg', '.jpeg'],
                    copy_grouped_pics_path : str = None, 
                    )->list: 
    
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


    # Load all files
    pic_paths = _load_images(path, name_filters_l)
    print(f'Loaded {len(pic_paths)} pictures after applying all filters')

    # pic by pic, load all exifs
    all_exifs = []
    for img in pic_paths:
        all_exifs.append( _get_exifs(img, path) )

    #sort them by date, form older to newer
    all_exifs.sort(key= lambda x: x['datetime_original'])

    # find groups of pictures taken in the same place, based on the
    # gps position and the threshold `max_thr_kms`
    initial = all_exifs[0]
    all_groups = []
    grouped = [initial]   
    counter = 0
    for k in range(1, len(all_exifs)): 
        actual = all_exifs[k]
        if('gps_latitude' not in actual or 'gps_longitude' not in actual):
            print("Latitude and/or longitude not found!")
            print(actual)
        else:
            (in_time, _) = _is_in_time( initial['datetime'], 
                                        actual['datetime'],
                                        max_thr_sec=min_seconds_threshold_similar)
            (closer, _) = _is_closer_than_n_kms( (initial['gps_latitude'], initial['gps_longitude']), 
                                        (actual['gps_latitude'], actual['gps_longitude']), 
                                        max_thr_kms= min_gps_threshold_similar) 
            
            if(not closer and not in_time):
                print(f"Found new group of {len(grouped)} pictures! ")
                #save all files in a new folder if we specify a path
                if(copy_grouped_pics_path is not None):
                    _save_copy_pics(path, grouped, copy_grouped_pics_path, counter)
                    counter +=1
                initial = actual
                all_groups.append(grouped)
                grouped = [initial]
            else:
                grouped.append( actual )
    all_groups.append(grouped)
    
    # Create final grouped mapping
    df = pd.DataFrame(columns=['start', 'end', 'lat', 'long', 'n_pics'])
    for group in all_groups:
        print(f"Exploring group of {len(group)} elements..")
        starting_date = group[0]['datetime']
        ending_date = group[-1]['datetime']
        lat_avg = mean( [_get_lat_long_decimal( (k['gps_latitude'], k['gps_longitude']) )[0] for k in group] )
        long_avg = mean( [_get_lat_long_decimal( (k['gps_latitude'], k['gps_longitude']) )[1] for k in group])
        print(f"Group has {len(group)} elements, goes from {starting_date} to {ending_date} and averages (lat,long) ({lat_avg}, {long_avg}).")
        df = pd.concat([df, pd.DataFrame([{'start':starting_date,'end':ending_date,'lat':lat_avg,'long':long_avg,'lat_dms': _dd2dms(lat_avg),'long_dms': _dd2dms(long_avg),'n_pics': len(group)}])], ignore_index=True)
    df.to_csv(path_or_buf=output_exif_map, index=False)
    print(f"File saved in {output_exif_map}")
    return (df, output_exif_map)




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

    # load all data
    allimg = _load_images(path, name_filters_l= name_filters_l)

    # read location mapping
    df_location_mapping = pd.read_csv(filepath_or_buffer=location_mapping_csv, header = 0)
    def convert_date_string(date_str):
        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    df_location_mapping.start = df_location_mapping.start.apply(convert_date_string)
    df_location_mapping.end = df_location_mapping.end.apply(convert_date_string)
    print(f"Loaded location mapping from {location_mapping_csv} and has {len(df_location_mapping)} rows")

    # get last date modified from file info
    allimg = [ (i, _get_image_modified_data(f"data/pics_whatsapp/{i}")) for i in allimg]

    # location mapping per file
    for img_data in allimg:
        #get corresponding exif data
        exif_data_to_insert = _map_location_mapping(img_data[1], df_location_mapping)
        print(f"Exif data found {exif_data_to_insert}")

        #open original file
        original_image_path = f"{path}/{img_data[0]}"
        print(f"Opening image from {original_image_path}")
        with open(original_image_path, 'rb') as img_file:
            img = Image(img_file)

        # append exif data
        if(exif_data_to_insert['lat'] is not None): img.gps_latitude = exif_data_to_insert['lat']
        if(exif_data_to_insert['long'] is not None): img.gps_longitude = exif_data_to_insert['long']
        if(exif_data_to_insert['date_str'] is not None): 
            img.datetime = exif_data_to_insert['date_str']
            img.datetime_original = exif_data_to_insert['date_str']
            img.datetime_digitized = exif_data_to_insert['date_str']
        
        # Save image with modified EXIF metadata to an image file
        folder_path_out = f'{output_image_path}/{img_data[0]}'
        print(f"Saving new image in {folder_path_out}")
        with open(folder_path_out, 'wb') as new_image_file:
                new_image_file.write(img.get_file())

        new_access_time_seconds = exif_data_to_insert['date'].timestamp()
        new_modified_time_seconds = exif_data_to_insert['date'].timestamp()
        os.utime(folder_path_out, times=(new_access_time_seconds, new_modified_time_seconds))
    

