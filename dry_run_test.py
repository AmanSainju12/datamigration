import pytest
from test import file_upload


@pytest.fixture
def minio_client_mock(mocker):
    # Mock the Minio client
    minio_client_instance = mocker.Mock()

    # Mock the fput_object method to return a mock object
    minio_client_instance.fput_object.return_value = mocker.Mock()

    return mocker.patch("test.Minio", return_value=minio_client_instance)


def test_file_upload_dry_run_success(minio_client_mock, capsys):
    # Call the file_upload function
    file_upload()

    # Assert that the Minio client was created with the correct parameters
    minio_client_mock.assert_called_once_with(
        endpoint="localhost:9000",
        access_key="t7y47zWNUw1VIjpZCIme",
        secret_key="mpWDvV0zU4PaNZUH6crycxafqaUksBIj8Is2YrXE",
        secure=False,
    )

    # Assert that the fput_object method was called with the correct parameters
    minio_client_instance = minio_client_mock.return_value
    minio_client_instance.fput_object.assert_called_once_with(
        "test-bucket",
        object_name="object-name.txt",
        file_path="C:/Users/aman.sainju/Desktop/test.txt",
        part_size=5 * 1024 * 1024  # Adjust as needed
    )

    # Assert that the "Dry run successful. File can be uploaded." message was printed
    # Capture printed output and assert the message
    captured = capsys.readouterr()
    assert "Dry run successful. File can be uploaded." in captured.out

# def test_file_upload_dry_run_failure(minio_client_mock, capsys):
#     # Mock the fput_object method to simulate a failure
#     minio_client_instance = minio_client_mock.return_value
#     minio_client_instance.fput_object.side_effect = Exception
#
#     # Call the file_upload function
#     file_upload()
#
#     # Assert that the Minio client was created with the correct parameters
#     minio_client_mock.assert_called_once_with(
#         endpoint="localhost:9000",
#         access_key="t7y47zWNUw1VIjpZCIme",
#         secret_key="mpWDvV0zU4PaNZUH6crycxafqaUksBIj8Is2YrXE",
#         secure=False,
#     )
#
#     # Assert that the fput_object method was called with the correct parameters
#     minio_client_instance.fput_object.assert_called_once_with(
#         "test-bucket",
#         object_name="object-name.txt",
#         file_path="C:/Users/aman.sainju/Desktop/test.txt",
#         part_size=5 * 1024 * 1024,
#     )
#
#     # Assert that the error message was printed
#     captured = capsys.readouterr()
#     assert "Dry run successful. File can be uploaded." in captured.out
#
#     # Print a success message
#     print("Test passed: Error message found in the output.")
