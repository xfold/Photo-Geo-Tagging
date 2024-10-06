from exif import Image as ExifImage
import os
import re
import datetime

class ImageProcessor:
    def get_filename_from_path(self, file_path: str) -> str:
        """
        Extracts the filename from a full file path.

        Args:
            file_path (str): The full file path.

        Returns:
            str: The extracted filename.
        """
        return os.path.basename(file_path)

    def list_pic_files_in_folder(self, folder_path: str, filters: list = ['jpg', 'jpeg']) -> list:
        """
        Lists picture files with specified file extensions in a folder.

        Args:
            folder_path (str): The path to the folder.
            filters (list): A list of file extensions to filter.

        Returns:
            list: A list of picture files in the folder.
        """
        jpg_and_jpeg_files = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(tuple(filters)):
                    jpg_and_jpeg_files.append(os.path.join(folder_path, filename))
        else:
            print(f"Folder '{folder_path}' does not exist or is not a directory.")
        return jpg_and_jpeg_files

    def extract_datetime_from_title(self, filename: str, filter_extensions: list = None) -> datetime.datetime:
        """
        Extracts datetime information from a filename based on a specified pattern.

        Args:
            filename (str): The filename to extract datetime from.
            filter_extensions (list): A list of file extensions to filter.

        Returns:
            datetime.datetime or None: The extracted datetime object, or None if not found.
        """
        if filter_extensions is None:
            filter_extensions = ['jpg', 'jpeg']

        pattern = r'IMG-(\d{8})-WA\d{4}\.(' + '|'.join(filter_extensions) + ')'
        match = re.search(pattern, filename, re.IGNORECASE)  # Case-insensitive match

        if match:
            date_str = match.group(1)
            try:
                datetime_obj = datetime.datetime.strptime(date_str, '%Y%m%d')
                return datetime_obj
            except ValueError:
                return None
        else:
            return None

    def clone_and_save_with_exif(self, original_filename: str, output_filename: str, datetime_obj: datetime.datetime) -> None:
        """
        Clones an image, updates its EXIF data with a new datetime, and saves it.

        Args:
            original_filename (str): The path to the original image.
            output_filename (str): The path to save the cloned image with modified EXIF data.
            datetime_obj (datetime.datetime): The new datetime object for EXIF data.
        """
        with open(original_filename, 'rb') as img_file:
            img = ExifImage(img_file)
        # Append exif data
        datetime_str = datetime_obj.strftime('%Y:%m:%d %H:%M:%S')
        img.datetime = datetime_str
        img.datetime_original = datetime_str
        img.datetime_digitized = datetime_str
        # Save image with modified EXIF metadata
        with open(output_filename, 'wb') as new_image_file:
            new_image_file.write(img.get_file())
        new_access_time_seconds = datetime_obj.timestamp()
        new_modified_time_seconds = datetime_obj.timestamp()
        os.utime(output_filename, times=(new_access_time_seconds, new_modified_time_seconds))

    def process_images_with_exif(self, folder_path: str, folder_path_exif: str, filters: list, verbose:bool=False) -> None:
        """
        Processes images in a folder, updates their EXIF data, and saves them in another folder.

        Args:
            folder_path (str): The path to the folder containing images.
            folder_path_exif (str): The path to the folder where modified images with EXIF data will be saved.
            filters (list): A list of file extensions to filter.
        """
        image_files_path = self.list_pic_files_in_folder(folder_path, filters=filters)
        print(image_files_path)
        print([self.get_filename_from_path(f) for f in image_files_path])

        for im_path in image_files_path:
            filename = self.get_filename_from_path(im_path)
            out_path = os.path.join(folder_path_exif, filename)
            dt_obj = self.extract_datetime_from_title(filename, filter_extensions=filters)
            
            if dt_obj:
                self.clone_and_save_with_exif(im_path, out_path, dt_obj)
                if(verbose):
                    print(f"Processing {filename}, as date {dt_obj}...")
            else:
                print(f"No datetime found in '{filename}'")


