from minio import Minio
from minio.error import S3Error
from helpers.logger import Logger


try:
    client = Minio(
        endpoint="localhost:9000",
        access_key="t7y47zWNUw1VIjpZCIme",
        secret_key="mpWDvV0zU4PaNZUH6crycxafqaUksBIj8Is2YrXE",
        secure=False,
    )
except S3Error as s3_error:
    Logger.write_log(f"{s3_error}", "error")

