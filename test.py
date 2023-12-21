from minio import Minio
from minio.error import S3Error


def file_upload():
    client = Minio(
        endpoint="localhost:9000",
        access_key="t7y47zWNUw1VIjpZCIme",
        secret_key="mpWDvV0zU4PaNZUH6crycxafqaUksBIj8Is2YrXE",
        secure=False,
    )
    bucket_name = "test-bucket"
    directory = "C:/Users/aman.sainju/Desktop/test.txt"
    try:
        # Perform a dry run to check if the file can be uploaded
        client.fput_object(
            bucket_name,
            object_name="object-name.txt",
            file_path=directory,
            part_size=5 * 1024 * 1024  # 5 MB part size, adjust as needed
        )
        print("Dry run successful. File can be uploaded.")
    except S3Error as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        file_upload()
    except KeyboardInterrupt as keyboard_interrupt:
        print(f"error: Program terminated")
