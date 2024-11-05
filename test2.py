import os

file_name = 'test.txt'
r,ext = os.path.splitext(file_name)
print(r,ext)