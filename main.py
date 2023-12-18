from minio_tools.api import create_bucket, list_bucket


def main():
    # Create an instance of the custom class

    # Invoke methods or access attributes
    bucket_name = "my-1st-bucket"
    is_created = create_bucket(bucket_name)
    if is_created:
        print(f"{bucket_name} bucket is created successfully")
    else:
        print(list_bucket())


if __name__ == "__main__":
    main()
