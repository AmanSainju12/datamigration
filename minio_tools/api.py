from . import client
from os import path


def create_bucket(bucket_name):
    is_exist = client.bucket_exists(bucket_name)
    if is_exist:
        return False
    else:
        client.make_bucket(bucket_name, "central-nepal", object_lock=False)
        return True


def list_bucket():
    try:
        return client.list_buckets()
    except Exception as e:
        print(f"list_bucket other_error: {e}")


def file_upload(local_file_path, bucket_name, file_name):
    result = client.fput_object(bucket_name, file_name, local_file_path)
    object_info = {"path": path.join(result.bucket_name, result.object_name), "e_tag": result.etag,
                   "name": result.object_name, "bucket_name": result.object_name, "last_modified": result.last_modified}
    return object_info
