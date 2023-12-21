from helpers.logger import Logger
from helpers.utils import get_file_paths, calculate_md5, get_object_name
from minio_tools.api import create_bucket, object_upload, list_object
from concurrent.futures import ThreadPoolExecutor
import time


class Program:
    def __init__(self):
        # creating instance for logger
        self.bucket_name = "my-1st-bucket"
        self.directory = "C:/Users/aman.sainju/Desktop/test"
        # self.directory = os.path.join(os.getcwd(), "files").replace("\\", "/")
        # return file path of the files from the given directory
        self.file_paths = sorted(get_file_paths(self.directory))
        self.start_index = 0

    def file_upload(self):
        is_success = False
        is_created = create_bucket(self.bucket_name)
        if is_created:
            Logger.write_log(f"{self.bucket_name} bucket is created successfully", "info")
        try:
            uploaded_object = list_object(self.bucket_name)  # get the list of uploaded objects from bucket
            obj_list = list(uploaded_object)
            # set current index of the uploaded object list
            self.start_index = len(obj_list) - 1
            # check if last uploaded file is corrupted if corrupted set start index with that index
            if calculate_md5(self.file_paths[self.start_index]) == obj_list[self.start_index].etag:
                self.start_index = len(obj_list)
        except Exception as e:
            Logger.write_log(e, "info")
        is_success = self._parallel_upload_to_s3(self.file_paths, self.bucket_name)
        return is_success

    def _parallel_upload_to_s3(self, files, bucket_name):
        is_success = False
        root_directory = self.directory.replace(self.directory.split("/")[-1], "")
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for index in range(self.start_index, len(files)):
                    file_path = files[index]
                    md5_checksum = calculate_md5(file_path)
                    object_key = get_object_name(file_path.replace(root_directory, ""))
                    futures.append(
                        {"object_info": executor.submit(object_upload, file_path, bucket_name, object_key),
                         "hash": md5_checksum})
                # Wait for all uploads to complete
                for future in futures:
                    future["object_info"].result()
                    if future["object_info"].result()["e_tag"] != future["hash"]:
                        Logger.write_log(
                            f"{future["object_info"].result()["name"]} is corrupted", "critical")
            is_success = True
        except KeyboardInterrupt as key_interrupt:
            Logger.write_log("Program terminated", "error")
            is_success = False
        except Exception as e:
            Logger.write_log(f"{e}", "error")
            is_success = False
        return is_success
