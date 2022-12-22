# <u>F</u>ile <u>A</u>utomated <u>A</u>ssistant <u>M</u>over

Welcome to the FREE File Automated Assistant Mover program! This program is designed to help you easily search, manage, and organize your files.

# Features

  - Organize your files into different folders based on their extension categories using the "Organize Folder" feature.
  - Search for files by name using the "Search by Word Name" feature.
  - Filter files by date modified using the "Search by Date Modified" feature. You can specify a range of dates to include or exclude from your search results.
  - Copy, move, or delete files using the "Copy/Move/Delete Files" feature.
  - Search for files by their content using the "Search by File Content" feature. This allows you to find files that contain specific words or phrases. Currently supporting excel, pdf, word, and text file searches.
  - Inspect the properties of a file and preview its contents using the "Inspect Files" feature.
  - Filter files by the numbers in their names using the "Search by Min & Max Number" in file name feature. You can specify a range of numbers to include or exclude from your search results.
  - Zip up files using the "Zip Up Files" feature. This allows you to easily compress and download multiple files at once.
  - Search for files by their extension using the "Search by File Extension" feature.
  - 100 file extensions are supported for folder organization!

# Requirements

- __Python 3__

This program is to meant to be ran in the terminal by entering this code in the same working directory where the program is located by typing:
```python faam.py```

If you are having trouble with the UTF-8 encoding when starting the program, first go into the current working directory where the program is located within the terminal.

Then if you're using the git bash terminal, you can try using the following command:

```PYTHONIOENCODING=utf-8 python faam.py```

### Dependencies

These are the modules you would need to install on your computer to run this program. You can go into your terminal and type "pip" followed by the module name below. If you don't have pip installed already, type "cmd" in your windows search bar to open the terminal. Then type:
```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```

followed by

```python get-pip.py```

### Modules needed

- __Zipfile__: A Python module for working with ZIP archive files.
- __PyPDF2__: A Python library for working with PDF documents.
- __Pandas__: A powerful and flexible data analysis and manipulation library for Python. Used for the Excel files here.
- __Docx__: A Python library for working with Microsoft Word documents.

# Easy organization for your files

If you have thousands of messy unorganized files, then this is one of the quickest ways to organize them into similar categories. First click on "copy as path" on the folder you want to organize, like in this picture:

![Folder Path](source_folder_test\source_path_pic.png)

In your terminal, go into your working directory where this program is located, then type:

```python faam.py C:\Enter\Your\Messy\Folder\Path```

or you can just right click and paste the path you just copied after the ```python faam.py```

__Before__:

![Before Pic](source_folder_test\before-organization-pic.png)

__After__:

![After Pic](source_folder_test\after-organization-pic.png)
![Terminal Pic](source_folder_test\terminal-photo.png)
