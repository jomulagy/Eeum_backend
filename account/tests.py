import os
import random
from django.test import TestCase

# Create your tests here.
current_directory = os.getcwd()  # 현재 디렉토리의 경로
parent_directory = os.path.dirname(current_directory)
print(parent_directory)
folder_name = "강아지"  # 찾을 폴더의 이름
search_path = os.path.join(parent_directory,"media\\profile")  # 검색을 시작할 경로
print(search_path)
for dirs in os.listdir(search_path):
    print(dirs)
    if dirs == folder_name:
        found_folder_path = os.path.join(search_path, folder_name)
        break
    else:
        found_folder_path = None
random_choice = random.choice([0, 1])

print(os.listdir(found_folder_path)[random_choice])
