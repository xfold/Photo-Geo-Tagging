import argparse
from src.ImageProcessor import ImageProcessor

def main():
    parser = argparse.ArgumentParser(description='Process images with EXIF data.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing images.')
    parser.add_argument('folder_path_exif', type=str, help='Path to the folder to save processed images.')
    parser.add_argument('filters', type=str, nargs='+', help='List of image file extensions to filter by.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')

    args = parser.parse_args()

    processor = ImageProcessor()
    processor.process_images_with_exif(args.folder_path, args.folder_path_exif, args.filters, verbose=args.verbose)

if __name__ == '__main__':
    main()