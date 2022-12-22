import os
import datetime
import time
from .cfinder import preview

def sort_files_by_date(directory_path, days, outside_range=False):
    # Sorts the files in the given directory by the date they were last modified and checks if the directory path is valid
    if not os.path.exists(directory_path):
        print('Invalid location. Please enter a valid directory path.')
        return
    current_time = time.time()
    files = os.listdir(directory_path)
    # Sorts the files by the date they were last modified
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))
    if outside_range == 'more': # Keeps only the files that were modified more than the specified number of days ago
        print(f'Files modified more than the last {int(days)} days:')
        sorted_files = [file for file in sorted_files if os.path.getmtime(os.path.join(directory_path, file)) < current_time - (days * 86400)]
    else: # Keeps only the files that were modified within the specified number of days
        print(f'Files modified within the last {int(days)} days:')
        sorted_files = [file for file in sorted_files if os.path.getmtime(os.path.join(directory_path, file)) >= current_time - (days * 86400)]
    directory_path = sorted_files
    return directory_path


def file_inspect(matching_files, files, source_dir, target):
    current_files = []
    if target == 'Matching Files':
        current_files = matching_files
        # If there are no matching files, exit the function
        if not matching_files:
            print('No matching files found.')
            return
    elif target == 'Source Files':
        current_files = files
        # If there are source files, exit the function
        if not files:
            print('No source files found.')
            return

    # Prints the index and name of each file in the matching_files list
    for i, file in enumerate(current_files):
        print(f'{i+1}. {os.path.basename(file)}')

    # Prompts the user to choose a file to inspect
    while True:
        file_num = input(
            f'\nCurrently Targetting: {target}\nEnter the number of the file you want to inspect, or enter "0" to return to main menu:\n ')
        try:
            file_num = int(file_num)
            if file_num == 0:
                break
            elif file_num > len(current_files):
                print('Invalid input. Please enter a valid number.')
            else:
                # Get the file the user selected
                file = os.path.join(source_dir, current_files[file_num-1])
                break
        except ValueError:
            print('Invalid input. Please enter a valid number.')
    if int(file_num) != 0:
        # Prints the properties of the selected file
        file_stats = os.stat(file)
        print(f'{"⧓" * 100}')
        print(f'\nName:            {file}')
        # Represents the size of the file in bytes.
        print(f'Size:            {file_stats.st_size} bytes') 
        # Represents the time of most recent metadata change on Unix and creation time on Windows. It is expressed in seconds.
        print(f'Created:         {datetime.datetime.fromtimestamp(file_stats.st_ctime)}') 
        # Represents the time of most recent access. It is expressed in seconds. 
        print(f'Last Accessed:   {datetime.datetime.fromtimestamp(file_stats.st_atime)}')
        # Represents the time of most recent content modification. It is expressed in seconds.
        print(f'Modified:        {datetime.datetime.fromtimestamp(file_stats.st_mtime)}')
        # Represents the time of most recent metadata change on Unix and creation time on Windows. It is expressed in seconds.
        print(f'Metadata Change: {datetime.datetime.fromtimestamp(file_stats.st_ctime)}')
        # Represents file type and file mode bits (permissions).
        print(f'File Type:       {datetime.datetime.fromtimestamp(file_stats.st_mode)}')
        print(f'\n{"⧓" * 100}')
        preview(file)
        # Prompts the user to remove the file or rename it
        while True:
            action = input(
                '\n\nWould you like to remove or rename this file? (Enter "remove", "rename", or "0" to exit): \n\n')
            if action.lower() == 'remove':
                remove_from_where = input(f'(BEWARE: Removing from source files is PERMANENT)\nRemove {file} from "matching" or "source" files?: ')
                if remove_from_where.lower() == 'source':
                    try:
                        os.remove(os.path.join(source_dir, file))
                        print(f'Removed {file} from the Source folder.')
                        # Remove the file from the matching_files list
                        current_files.remove(file)
                        files = current_files
                        return current_files
                    except Exception as e:
                        print(f'Error: {e} ')
                    input('Returning to the main menu.')
                    return files, matching_files
                elif remove_from_where.lower() == 'matching':
                    try:
                        current_files.remove(file)
                        print(f'Removed {file} from the Matching files list.')
                        files = matching_files
                        return matching_files
                    except Exception as e:
                        print(f'Error: {e} ')
            elif action.lower() == 'rename':
                new_name = input('Enter the new name for the file: ')
                ext = os.path.splitext(file)[1].strip('.')
                # Example: This renames the full path file from "C:\Users\user\Desktop\flyers\60 cat dogs.txt" to "C:\Users\user\Desktop\flyers\90 dog cats.txt"
                os.rename(os.path.join(source_dir, file), os.path.join(source_dir, (new_name + '.' + ext)))
                print(f'Renamed {file} to {new_name}.')
                input('Returning to the main menu.')
                break
            elif action.lower() == '0':
                input('Returning to the previous menu...')
                break
            else:
                print('Invalid input. Please enter a valid command.')
    else:
        pass



