##清除空文件夹
import os
def delnulldir(path):
    dir_list = os.listdir(path)
    for dir in dir_list:
        null_dir_path = path + '/' +dir
        dir_size = os.stat(null_dir_path).st_size
        if dir_size == 68:
            os.rmdir(null_dir_path)
        print("==============="+null_dir_path+" has been removed=============")
    #print(dir_list)
delnulldir("/Volumes/100G(HDD)/mzitu")