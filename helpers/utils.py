import os
import hashlib
from concurrent.futures import ThreadPoolExecutor
from minio_tools.api import object_upload


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


def parallel_upload_to_s3(files, bucket_name, directory):
    root_directory = directory.replace(directory.split("/")[-1], "")

    with ThreadPoolExecutor() as executor:
        futures = []
        for file_path in files:
            md5_checksum = calculate_md5(file_path)
            object_key = file_path.replace(root_directory, "")
            # print(f"object_key: {object_key}")
            futures.append(
                {"object_info": executor.submit(object_upload, file_path, bucket_name, object_key), "hash": md5_checksum})

        # Wait for all uploads to complete
        for future in futures:
            future["object_info"].result()
            print(future["object_info"].result())
            if future["object_info"].result()["e_tag"] != future["hash"]:
                print(f"file corrupted: {future["object_info"].result()["name"]}")
