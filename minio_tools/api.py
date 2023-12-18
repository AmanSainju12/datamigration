from . import client


def create_bucket(bucket_name):
    is_exist = client.bucket_exists(bucket_name)
    if is_exist:
        return False
    else:
        client.make_bucket(bucket_name, "central-nepal", object_lock=True)
        return True


def list_bucket():
    return client.list_buckets()
