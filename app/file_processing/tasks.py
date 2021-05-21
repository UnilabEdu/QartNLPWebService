from app import celery
import shutil
import time


@celery.task()
def copy_files(file_path):
    split_file = file_path.split('.')

    for i in range(5):
        copied_file = split_file[0] + str(i) + "." + split_file[1]
        shutil.copy(file_path, copied_file)
        print("Working...")
        time.sleep(2)