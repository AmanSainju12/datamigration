import argparse
import os


def create_files(no_of_files: int):
    os.mkdir(os.path.join(os.getcwd(), "files"))
    for i in range(0, no_of_files):
        file_handler = open(os.path.join(os.getcwd(), "files", f"file-{i}.txt"), "w+")
        file_handler.write(str(i))
        file_handler.close()


# Create ArgumentParser object
parser = argparse.ArgumentParser(description='A script to generate txt files')

# Add named arguments
parser.add_argument('--count', help='number of files to generate')

# Parse the command line arguments
args = parser.parse_args()

# Access the values of the named arguments
count = args.count

# Print the values
print('number of files to generate:', count)
create_files(int(count))
