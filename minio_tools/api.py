import time
from . import client
from os import path
from minio.error import S3Error
from helpers.logger import Logger


def create_bucket(bucket_name):
    try:
        is_exist = client.bucket_exists(bucket_name)
        if is_exist:
            return False
        else:
            client.make_bucket(bucket_name, "central-nepal", object_lock=False)
            return True
    except Exception as e:
        Logger.write_log(f"{e}", "error")


def list_bucket():
    try:
        return client.list_buckets()
    except Exception as e:
        Logger.write_log(f"list_bucket other_error: {e}", "error")


def object_upload(local_file_path, bucket_name, file_name):
    try:
        time.sleep(1)
        result = client.fput_object(bucket_name, file_name, local_file_path)
        object_info = {"path": path.join(result.bucket_name, result.object_name), "e_tag": result.etag,
                       "name": result.object_name, "bucket_name": result.object_name,
                       "last_modified": result.last_modified}
        return object_info
    except FileNotFoundError as file_not_found:
        Logger.write_log(
            f"{file_not_found}", "info")
    except S3Error as s3_error:
        Logger.write_log(
            f"{s3_error}", "error")
    except KeyboardInterrupt:
        Logger.write_log("Program Terminated", "critical")
    except Exception as e:
        Logger.write_log(e, "error")


def object_stat(bucket_name, object_key):
    try:
        client.stat_object(bucket_name, object_key)
        return True
    except S3Error as s3_error:
        Logger.write_log(f"{s3_error}", "error")
        return False


def list_object(bucket_name, prefix=None):
    result = client.list_objects(bucket_name, prefix, recursive=True)
    return result
