import time
from minio_tools.api import create_bucket, file_upload
from helpers.utils import get_file_paths, get_object_name, calculate_md5


def main():
    file_upload_count = 0
    try:
        open_upload_count_txt = open("upload_count.txt", "r")
        file_upload_count = int(open_upload_count_txt.read())
    except Exception as e:
        print(e)

    directory = "C:/Users/aman.sainju/Desktop/test"

    # return file path of the files from the given directory
    file_paths = get_file_paths(directory)
    bucket_name = "my-1st-bucket"
    is_created = create_bucket(bucket_name)
    if is_created:
        print(f"{bucket_name} bucket is created successfully")

    root_directory = directory.replace(directory.split("/")[-1], "")
    for index in range(file_upload_count, len(file_paths)):
        path = file_paths[index]
        md5_checksum = calculate_md5(path)
        try:
            # time.sleep(2)
            object_name = get_object_name(path.replace(root_directory, ""))
            object_info = file_upload(path, bucket_name, object_name)
            file_upload_count += 1
            if object_info["e_tag"] != md5_checksum:
                print(f"{md5_checksum} {object_info["e_tag"]}")
                print(f"file currupted: {object_info["name"]}")
            upload_count_txt = open("upload_count.txt", "w+")
            upload_count_txt.write(str(file_upload_count))
            upload_count_txt.close()
        except Exception as e:
            print(f"file-upload-error: {e}")
            upload_count_txt = open("upload_count.txt", "w+")
            upload_count_txt.write(str(file_upload_count))
            upload_count_txt.close()
            break


if __name__ == "__main__":
    main()
