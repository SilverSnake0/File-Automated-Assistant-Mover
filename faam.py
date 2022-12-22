import os
import shutil
import sys
import zipfile
from modules.forganizer import organize, arg_cleaner
from modules.cfinder import search_by_content
from modules.finspect import file_inspect, sort_files_by_date

# Checks if pip is installed
try:
    import pip
except ImportError:
    # Install pip using get-pip.py
    os.system('curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py') # Pip is a package manager for Python. It is a tool that allows you to install, upgrade, and manage packages.
    os.system('python get-pip.py')

# Checks if the dependencies are installed
dependencies = ['PyPDF2', 'pandas', 'docx', 'zipfile']
missing_dependencies = []
for dependency in dependencies:
    try:
        __import__(dependency)
    except ImportError:
        missing_dependencies.append(dependency)

# If there are missing dependencies, this asks the user if they want to install them
if missing_dependencies:
    print(f'The following dependencies are missing: {missing_dependencies}')
    install = input('Do you want to install them now? ("yes" or "no") ')
    if install.lower() == 'yes':
        # Installs the missing dependencies using pip
        for dependency in missing_dependencies:
            os.system(f'pip install {dependency}')
    else:
        print('Please note that some of the functions in this program may not work due to missing dependencies, and may cause the program to unexpectedly terminate or cause errors.')

# Defines the global variables
matching_files = []
target = 'Source Files'

try:
    # Defines the source and destination directories
    # You can enter your source directory path here if you don't want to enter it each time you run the program
    source_dir = "C:\\Enter\\Your\\Source\\Folder\\Path" 
    # You can enter your destination directory path here if you don't want to enter it each time you run the program
    destination_dir = "C:\\Enter\\The\\Destination\\Path"
        
    # Gets a list of files in the source directory
    files = os.listdir(source_dir)
except:
    pass

def rename_folders(source_dir, destination_dir, files):
    source_folder = input(
        f'\n\n(Current Source Folder: {source_dir})\n\nPlease enter the new source folder path if you wish to change it, or enter ("no" or "0") to cancel: \n')
    if source_folder in ('0', 'no'):
        pass
    else:
        try:
            # Fixes the source path link if OS is windows
            source_folder = arg_cleaner(source_folder)
            files = os.listdir(source_folder)
            # Define the new source and directories
            source_dir = source_folder
            print(f'Successfully changed source to {source_folder}!')
        except Exception as e:
            print(e)

    destination_folder = input(
        f'\n\n(Current Destination Folder: {destination_dir})\n\nPlease enter the new destination folder path if you wish to change it, or enter ("no" or "0") to cancel: \n')
    if destination_folder in ('0', 'no'):
        pass
    else:
        # Fixes the source path link if OS is windows
        destination_folder = arg_cleaner(destination_folder)
        # Creates the destination folder if it does not exist
        os.makedirs(destination_folder, exist_ok=True)
        # Defines the new destination folder
        destination_dir = destination_folder
        print(f'Successfully changed {destination_dir} to {destination_folder}!')
    return source_dir, destination_dir, files

def copy_files(file):
    try:
        # Checks if the source and destination are the same
        if os.path.abspath(source_dir) == os.path.abspath(destination_dir):
            print(
                f'Skipping copy of "{file}" because the source and destination are the same.')
        else:
            print('copying...')
            # Copy the file to the destination directory
            if file in destination_dir:
                print(f'This already exists in the destination folder. Skipped {file}.')
            else:
                shutil.copy(file, destination_dir)
                print(f'Copied files successfully!')
    except Exception as e:
            print(f'Error: {e}')

def move_files(file):
    try:
        # Checks if the source and destination are the same
        if os.path.abspath(source_dir) == os.path.abspath(destination_dir):
            print(
                f'Skipping move of "{file}" because the source and destination are the same.')
        else:
            print('moving...')
            # Moves the file to the destination directory
            try:
                shutil.move(file, destination_dir)
                print(f'Moved files successfully!')
            except:
                print(f'File already exists... skipping {file}')
    except Exception as e:
            print(f'Error: {e}')

def remove_files(file):
    try:
        # Checks if the source and destination are the same
        if os.path.abspath(source_dir) == os.path.abspath(destination_dir):
            print(
                f'Skipping move of "{file}" because the source and destination are the same.')
        else:
            print('deleting...')
            # Deletes the file to the destination directory
            os.remove(file)
            print(f'Deleted files successfully!')
    except Exception as e:
            print(f'Error: {e}')

# Gives the ability to place the copied or moved files into a new folder renamed to their choosing
def package_move(matching_files, action):
    count = 0
    # If there are no matching files, exit the function
    if not matching_files:
        return
    # Prompts the user to enter the name of the folder
    folder_name = input('\nEnter the name of the folder you wish to create: ')

    # Creates the folder in the destination directory
    folder_path = os.path.join(destination_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Moves the files to the folder
    for file in matching_files:
        if action.lower() == 'move':
            print(f'Attempting to move "{file}"...')
            count += 1
            file_name = os.path.basename(file) # function is used to extract the file name from the file path
            destination = os.path.join(folder_path, file_name)
            os.rename(file, destination)
        else:
            print(f'Attempting to copy "{file}"...')
            count += 1
            file_name = os.path.basename(file) # function is used to extract the file name from the file path
            destination = os.path.join(folder_path, file_name)
            shutil.copy(file, destination)

    input(f'{count} files successfully transferred to the new folder located at {destination_dir}!')

def file_action(matching_files):
    # If there are no matching files, exit the function
    if not matching_files:
        return

    # Prompts the user to choose between copy and move
    while True:
        file_names = [os.path.basename(path) for path in matching_files]
        print(f'\nCurrent Matching Files: {file_names}')
        operation = input(
            f'\n{len(matching_files)} files are currently in the matching list.\n\n(Enter "copy", "move", "save", or "delete")\nWould you like to copy, move, save, or delete these files?\n')
        if operation.lower() == 'copy':
            package_ans = input(f'Would you like to create a new folder name for these files? ("yes" or "no")\n')
            if package_ans.lower() == 'yes':
                package_move(matching_files, operation)
                break
            else:
                # Copy the matching files to the destination directory
                for file in matching_files:
                    print(f'Attempting to copy "{file}"...')
                    copy_files(file)
                break

        elif operation.lower() == 'move':
            package_ans = input(f'Would you like to create a new folder name for these files? ("yes" or "no")\n')
            if package_ans.lower() == 'yes':
                package_move(matching_files, operation)
                matching_files = []
                break
            else:
            # Moves the matching files to the destination directory
                for file in matching_files:
                    print(f'Attempting to move "{file}"...')
                    move_files(file)
                    matching_files = []
                break

        elif operation.lower() == 'save':
            input('Saved files successfully!')
            print(matching_files)
            break

        elif operation.lower() == 'delete':
            are_you_sure = input(f'BEWARE: Deleting these files is PERMANENT\nAre you sure (enter "yes" or "no")?')
            if are_you_sure == 'yes':
                for file in matching_files:
                    print(f'Attempting to delete "{file}"...')
                    remove_files(file)
                    matching_files = []
                break
            else:
                print('Cancelled.')
                break
        else:
            input(f'Your input is not a valid option. Please try again.')

def search_by_extension(files, source_dir, target, matching_files):
    count = 0
    if target == 'Source Files':
        files = os.listdir(source_dir)
    else:
        files = matching_files
    # Prompt the user to enter a file extension to search for
    extension = input(f'Currently targetting: {target}\nWhat file extension would you like to search for?')
    # Search for files with the specified extension
    for file in files:
        if file not in matching_files:
            if file.endswith(extension):
                matching_files.append(file)
                count += 1
    file_names = [os.path.basename(path) for path in matching_files]
    print(f'Matching Files: {file_names}')
    input(f'\nSearch completed. Found {count} new matching files ending with {extension}!\n')
    return matching_files

def search_by_name(source_dir, matching_files, target):
    count = 0
    # Prompts the user for the word to search for in the file names
    search_word = input(
        f'Enter the word you want to search for within the "{target}": ')
    if target == 'Source Files':
        # Recursively search through all subfolders of the source directory
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file not in matching_files:
                    if search_word in file.strip().lower():
                        count += 1
                        print(f'Found matching {search_word} in {file}!')
                        # The file matches the search term, add it to the list of matching files
                        matching_files.append(os.path.join(root, file))
                else:
                    continue
        print(f'There are {count} files matching the word {search_word}.')
    else:
        new_matching_files = []
        for file in source_dir:
            if search_word in file.strip().lower():
                if file not in new_matching_files:
                    print(f'Found matching {search_word} in {file}!')
                    new_matching_files.append(os.path.join(source_dir, file))
                    count += 1
        matching_files = new_matching_files
        print(f'There are {count} files matching the word {search_word}.')
        return matching_files

    file_action(matching_files)

def search_by_num(source_dir, matching_files):
    # Prompt the user for the minimum and maximum number range
    while True:
        try:
            min_range = int(input('Enter the minimum number: '))
            max_range = int(input('Enter the maximum number: '))
            if min_range > max_range:
                print(f'The minimum number must be less than or equal to the maximum number. Please try again.')
            else:
                break
        except ValueError:
            print(f'You must enter a valid number. Please try again.')

    # Recursively search through all subfolders of the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file not in matching_files:
                # Splits the file name into a list of words
                words = file.split()
                for word in words:
                    # Checks if the word is a number within the specified range
                    if word.isdigit() and min_range <= int(word) <= max_range:
                        # The word is a number within the specified range
                        matching_files.append(os.path.join(root, file))
                        break
            else:
                continue
    file_action(matching_files)

def compress(source_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zip_obj:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zip_obj.write(file_path, arcname=arcname)
    return zip_file_path

def zipfiles():
    change_target_ans = input(f'("Yes" or "No". Enter "0" to return to the main menu)\nWould you like to zip up the files in the Source folder:\n')
    if change_target_ans.strip().lower() == 'yes':
        label = input('What would you like to name the zip file as?')
        print('zipping up files...')
        zip_file_path = os.path.join(destination_dir, f'{label}.zip')
        compress(source_dir, zip_file_path)
        input('Zipping files has been completed successfully!')
    else:
        main_menu(target, matching_files, source_dir, destination_dir)

def main_menu(target, matching_files, source_dir, destination_dir):
    target = target
    current_num_files = 0
    # Gets a list of files in the source directory
    try:
        files = os.listdir(source_dir)
    except Exception as e:
        print(f'Error: {e}')
    try:
        len_matching_files = len(matching_files)
    except Exception as e:
        print(f'Error: {e}')
    try:
        for file in files:
            current_num_files += 1
    except Exception as e:
        print(f'Error: {e}. Please check your source and directory paths are correct. Program will terminate.')
        print('Exiting the program.')
        sys.exit(0)
    print('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
    print(f'▌              ███████╗ █████╗  █████╗ ███╗   ███╗    Current Source Directory Path:      {source_dir}')
    print(f'▌              ██╔════╝██╔══██╗██╔══██╗████╗ ████║    Current Destination Directory Path: {destination_dir}')
    print(f'▌              █████╗  ███████║███████║██╔████╔██║    Number of Files in Source Directory:          {current_num_files}')
    print(f'▌              ██╔══╝  ██╔══██║██╔══██║██║╚██╔╝██║    Number of Matching Files in Source Directory: {len_matching_files}')
    print(f'▌              ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    Targetting:                                   {target}')
    print('▌              ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝                                                                                 ▌')
    print('▌                File Automated Assistant Mover                                                                                    ▌')
    print('▌                Main Menu                                                                                                         ▌')
    print('▌                Please select from the following options by their number:                       0. EXIT                           ▌')
    print('▌                                                                                                                                  ▌')
    print('▌ 1. Change Target                                      2. Search by Name                        3. Search by Date Modified        ▌')
    print('▌ 4. Rename Source/Destination Path                     5. Copy/Move/Delete Files                6. Search by File Content         ▌')
    print('▌ 7. Reset                                              8. Inspect Files                         9. Search by Min & Max Number     ▌')
    print('▌10. Zip up files                                      11. Organize Folder                      12. Search by File Extension       ▌')
    print('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
    try:
        menu_answer = int(input('Please enter a number:\n'))
    except:
        main_menu(target, matching_files, source_dir, destination_dir)
    if menu_answer == 1:
        change_target_ans = input('\nWould you like to change the target to "Source" or "Matching" files?: \n')
        if change_target_ans.lower() == 'source':
            target = 'Source Files'
        elif change_target_ans.lower() == 'matching':
            target = 'Matching Files'
        else:
            print('Invalid target. Please try again.')
    elif menu_answer == 2:
        try:
            if target == 'Source Files':
                search_by_name(source_dir, matching_files, target)
            else:
                search_by_name(matching_files, matching_files, target)
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 3:
        try:
            outside_range = input(f'\nEnter one of the following options:\n1. Keep files > (more) than a specified number of days\nOR\n2. Keep files < (less) than a specified number of days?\n\nEnter "more" or less": ')
            days = input(f'Please enter the number of days: ')
            if target == 'Source Files':
                files = source_dir
                try:
                    new_list = sort_files_by_date(source_dir, int(days), outside_range)
                    for file in new_list:
                        matching_files.append(os.path.join(source_dir, file))
                except  Exception as e:
                    print(f'Error: {e}')
            elif target == 'Matching Files':
                matching_files = source_dir
                new_list = sort_files_by_date(source_dir, int(days), outside_range)
                for file in new_list:
                    matching_files.append(os.path.join(source_dir, file))
            file_names = [os.path.basename(path) for path in matching_files]
            print(f'Matching files by date modified: {file_names}')
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 4:
        try:
            source_dir, destination_dir, files = rename_folders(source_dir, destination_dir, files)
            print(f'Source: {source_dir}\nDestination: {destination_dir}')
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 5:
        file_action(matching_files)
    elif menu_answer == 6:
        try:
            string = input(f'[Search for word within file content]\nWhat would would you like to search for:')
            search_by_content(files, string, source_dir, target, matching_files)
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 7:
        matching_files = []
        target = 'Source Files'
    elif menu_answer == 8:
        try:
            file_inspect(matching_files, files, source_dir, target)
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 9:
        try:
            search_by_num(source_dir, matching_files)
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 10:
        try:
            zipfiles()
        except Exception as e:
            print(f'Error: {e}')
    elif menu_answer == 11:
        change_target_ans = input(f'\nWould you like to organize "Source" files or "Destination" files":\n')
        if change_target_ans.strip().lower() == 'source':
            organize(source_dir)
        elif change_target_ans.strip().lower() == 'destination':
            organize(destination_dir)
        else:
            print('Input is invalid. Please try again.')
    elif menu_answer == 12:
        try:
            search_by_extension(files, source_dir, target, matching_files)
        except:
            main_menu(target, matching_files, source_dir, destination_dir)
    elif menu_answer == 0:
        print('Exiting the program.')
        sys.exit(0)
    main_menu(target, matching_files, source_dir, destination_dir)
terminal_count = 1
if __name__ == '__main__':
    try:
        # Gets the directory path from the command line argument
        try: # Second Try and Except is added so that there won't be an error if the faam.py first terminal argument is missing.
            arg = sys.argv[1]
            arg_cleaner(arg)
            print('Organizing files...')
            terminal_count -= 1
            organize(arg)
        except:
            pass
    except Exception as e:
        # Prints an error message if there is an exception
        print(f'Error: {e}')
        print('Enter the following in the terminal to start the automatic file organization: python faam.py C:\\Enter\\your\\folder\\path\\here')
if terminal_count == 1: # This is checked so that the code below won't run if this program is called directly from the terminal with a path argument
    source_ans = input(f'Current Source Folder: {source_dir}\nPlease enter the new source directory path, or enter 0 to keep the current folder: \n')
    if source_ans != '0':
        if source_ans.startswith('"') and source_ans.endswith('"'):
            # Remove the double quotes from the path
            source_ans = source_ans[1:-1]
        source_dir = source_ans
    directory_ans = input(f'\nCurrent Destination Folder: {destination_dir}\nPlease enter the new destination directory path, or enter 0 to keep the current folder: ')
    if directory_ans != '0':
        if directory_ans.startswith('"') and directory_ans.endswith('"'):
            # Remove the double quotes from the path
            directory_ans = directory_ans[1:-1]
        destination_dir = directory_ans
        
    main_menu(target, matching_files, source_dir, destination_dir)
else:
    pass
