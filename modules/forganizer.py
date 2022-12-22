from .extensions import get_folder_name
import os
import shutil

def arg_cleaner(arg):
    if os.name == 'nt':
        # Checks if the provided path contains double quotes surrounding the path link
        if arg.startswith('"') and arg.endswith('"'):
            # Remove the double quotes from the path
            arg = arg[1:-1]
        # Checks if the provided path uses a single backslash
        elif '\\' in arg:
            # Replaces the single backslash with double backslashes
            arg = arg.replace('\\', '\\\\')
    return arg

def organize(directory_path):
    
    #Organizes all the files in the given directory by their file extensions.
    #Creates a new folder for each file extension and moves the corresponding files into that folder. If a folder with the same name already exists, it silently skips it.
    
    count = 0 # Count for the number of files moved

    if not os.path.exists(directory_path):
        print('Invalid location. Please enter a valid directory path.')
        return

    # Gets the list of files in the directory
    files = os.listdir(directory_path)
    
    # Creates a set of all the file extensions in the directory
    extensions = set(os.path.splitext(file)[1].strip('.') for file in files)

    # Creates new folder for each file extension, if it doesn't exist already
    for ext in extensions:
        folder_name = get_folder_name(ext)
        if folder_name:
            os.makedirs(os.path.join(directory_path, folder_name), exist_ok=True)

    # Moves the files to the corresponding folders
    for file in files:
        # Splits the file name and locates the extension at the end of the file name
        ext = os.path.splitext(file)[1].strip('.')
        folder_name = get_folder_name(ext)
        # Skips files that don't have a corresponding folder
        if not folder_name:
            continue

        destination = os.path.join(directory_path, folder_name, file)
        source = os.path.join(directory_path, file)

        # Only moves the file if it doesn't already exist in the destination folder
        if not os.path.exists(destination):
            shutil.move(source, destination)
            count += 1
            print(f'{file} moved to {folder_name}.')

    input(f'\nAll {count} files have been successfully organized and are located in your {directory_path} folder!')
