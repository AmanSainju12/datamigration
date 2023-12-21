import time
from minio.error import S3Error
from helpers.logger import Logger
from helpers.utils import get_file_paths, get_object_name, calculate_md5
from minio_tools.api import create_bucket, object_upload, object_stat, list_object


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
            print(self.start_index)
            # check if last uploaded file is corrupted if corrupted set start index with that index
            if calculate_md5(self.file_paths[self.start_index]) == obj_list[self.start_index].etag:
                start_index = len(list(uploaded_object))
        except Exception as e:
            Logger.write_log(e, "info")
            pass

        # parallel_upload_to_s3(file_paths, bucket_name, directory)

        # remove last path of directory
        root_directory = self.directory.replace(self.directory.split("/")[-1], "")
        print(self.start_index)
        try:
            # upload the file to storage with listed file_paths
            for index in range(self.start_index, len(self.file_paths)):
                path = self.file_paths[index]
                md5_checksum = calculate_md5(path)  # calculate checksum
                object_name = get_object_name(path.replace(root_directory, ""))
                # checking if uploading file is already exist in bucket if exist do not upload
                is_object_exist = object_stat(self.bucket_name, object_name)
                if is_object_exist:
                    Logger.write_log(
                        f"{object_name} already exist in the storage", "info")
                else:
                    object_info = object_upload(path, self.bucket_name, object_name)
                    # checking if the uploaded file is corrupted write log if corrupted
                    if object_info["e_tag"] != md5_checksum:
                        Logger.write_log(
                            f"{object_info["name"]} is corrupted", "critical")
                    Logger.write_log(
                        f"{object_info["name"]} is uploaded successfully", "info")
            is_success = True
        except FileNotFoundError as file_not_found:
            Logger.write_log(
                f"{file_not_found}", "info")
            is_success = False
        except S3Error as s3_error:
            Logger.write_log(
                f"{s3_error}", "error")
            is_success = False
        except KeyboardInterrupt as keyboard_interrupt:
            Logger.write_log("Program Terminated", "critical")
            is_success = False
        except Exception as e:
            Logger.write_log(e, "error")
            is_success = False
        return is_success
