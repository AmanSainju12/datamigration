from minio import Minio
from minio.error import S3Error


try:
    client = Minio(
        endpoint="localhost:9000",
        access_key="t7y47zWNUw1VIjpZCIme",
        secret_key="mpWDvV0zU4PaNZUH6crycxafqaUksBIj8Is2YrXE",
        secure=False,
    )
except S3Error as exe:
    print(f"Error: {exe}")
