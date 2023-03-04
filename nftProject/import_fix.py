file_path = '/usr/local/lib/python3.11/site-packages/parsimonious/expressions.py'

input_file = open(file_path, "r")

filedata = input_file.read()
input_file.close()
print()

filedata = filedata.replace('getargspec', 'getfullargspec')
print(filedata[:500])
print()

with open(file_path, "w") as f:
    f.write(filedata)
    f.close()

exit()