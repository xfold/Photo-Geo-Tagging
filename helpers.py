from exif import Image
import os
import math
from datetime import datetime, timedelta
import geopy.distance
from statistics import mean
import pandas as pd
import ast

def _load_images(path: str, name_filters_l : list = ['.jpg'] )->list: 
    allf = os.listdir(path)
    tor = []
    for str_filter in name_filters_l:
        allf_aux = [f for f in allf if str_filter in f]
        tor = tor + allf_aux
    return tor

def _get_exifs(filename : str,
               filepath : str,
               exifs_to_append: list = ['datetime','datetime_original','gps_altitude','gps_altitude_ref','gps_latitude','gps_latitude_ref','gps_longitude','gps_longitude_ref','model']
               )-> dict:

    path = f'{filepath}{filename}'
    d = {'filename':filename, 'filepath':filepath}
    with open(path, 'rb') as img_file:
        img = Image(img_file)
        for exif_prop in exifs_to_append:
            if(exif_prop) in img.list_all():
                d[exif_prop] = img.get(exif_prop)
    return d

def _dms2dd(degrees:float, minutes:float, seconds:float, direction='N'):
    """transform degrees, minutes, seconds coords into decimal coordinates"""
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd;

def _dd2dms(deg):
    """Convert from decimal degrees to degrees, minutes, seconds."""
    m, s = divmod(abs(deg)*3600, 60)
    d, m = divmod(m, 60)
    if deg < 0:
        d = -d
    d, m = int(d), int(m)
    return d, m, s


def _get_lat_long_decimal(lat_long:tuple):
    (lat, long) = lat_long   
    return (_dms2dd(lat[0], lat[1], lat[2]), _dms2dd(long[0], long[1], long[2]))

def _is_closer_than_n_kms(lat_long:tuple, 
                           lat2_long2 :tuple, 
                           max_thr_kms: float = .5)-> tuple: 
    
    #both lat and long are in this format -> (51.0, 23.0, 53.84) and need
    #to be trasnformed into decimal e.g. 12.13
    p1 = _get_lat_long_decimal(lat_long) 
    p2 = _get_lat_long_decimal(lat2_long2) 
    d = geopy.distance.geodesic(p1, p2).km
    return (d < max_thr_kms, d)

def _is_in_time(time_str_1:str,
                time_str_2:str, 
                max_thr_sec:float = 3600):
    
    dt1 = datetime.strptime(time_str_1, '%Y:%m:%d %H:%M:%S')
    dt2 = datetime.strptime(time_str_2, '%Y:%m:%d %H:%M:%S')
    time_diff = (dt2 - dt1).seconds
    return (time_diff<=max_thr_sec, time_diff)
    
def _save_copy_pics(path:str, 
                    grouped:list,
                    copy_grouped_pics_path:str,
                    counter:int):
    for p in grouped:
        original_path = path+p
        to_save = copy_grouped_pics_path+str(counter)+'_'+p
        #print(f"we will save file {original_path} in {to_save}")
        #This does not work as it says it cannot create a directory
        with open(original_path, 'rb') as a:
            img_a = Image(a)
        with open(to_save, 'wb') as b:
            b.write(img_a.get_file())

# get date modified from image
def _get_image_modified_data(path):
    # get the date last modified of the file
    date_modified = os.path.getmtime(path)
    # convert the timestamp to a datetime object
    date_modified = datetime.fromtimestamp(date_modified)
    date_modified_str = date_modified.strftime('%Y-%m-%d %H:%M:%S')
    return date_modified_str

# map location mapping
def _map_location_mapping(my_datetime_str, df):
    # boolean indexing to filter the rows
    my_datetime_str = my_datetime_str.replace('-', ':')
    my_datetime = datetime.strptime(my_datetime_str, '%Y:%m:%d %H:%M:%S')
    result = df[(df['start'] <= my_datetime) & (my_datetime <= df['end'])]
    return {'date_str':my_datetime_str ,'date': my_datetime, 'lat':None, 'long':None, 'lat_dec':None, 'long_dec':None} if len(result) == 0 else {'date_str':my_datetime_str,'date':my_datetime, 'lat':ast.literal_eval( result['lat_dms'].values[0]), 'long':ast.literal_eval( result['long_dms'].values[0]), 'lat_dec':result['lat'].values[0], 'long_dec':result['long'].values[0]}
   