import os
import hashlib


def get_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file).replace("\\", "/"))
    return file_paths


def get_object_name(path: str):
    return path


def calculate_md5(local_file_path):
    md5_hash = hashlib.md5()
    with open(local_file_path, "rb") as file:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


