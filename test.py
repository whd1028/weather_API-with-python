import pandas as pd

file = open("OpenAPI_Project\LocationCode.txt",'r',encoding='utf-8')
print(file)
x = file.read()
# x = file.readlines()
x = x.replace("\n\n",",")
x = x.replace("\n","")
x = x.replace(" ","")
x = x.split(',')
# print(x)
# print(type(x))
code = []
location = []
for i, v in enumerate(x):
    if i % 3 == 0:
        code.append(v)
    elif i % 3 == 1:
        location.append(v)
LocationCode = dict(zip(location,code))

print(f"LocationCode = {LocationCode}")
file.close()