import os 

filepath=r"C:\Users\Ashutosh\Desktop\using_elser\vectorstore_test.pdf"
filename=os.path.basename(filepath)
base,extension=os.path.splitext(filename)
print(base)
print(extension)