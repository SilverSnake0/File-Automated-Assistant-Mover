import os
import zipfile

def compress(source_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zip_obj:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zip_obj.write(file_path, arcname=arcname)
    return zip_file_path
