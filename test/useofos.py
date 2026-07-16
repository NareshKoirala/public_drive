import os

m_path = os.getcwd()

print(m_path, "\n", "-" * 10)  # to get the current path the file is running on

c_path = m_path + "/.."  # go back one space

os.chdir(
    c_path
)  # change the cwd of the program so instead of running in the path that inital was we change to a different one


print(os.getcwd(), "\n", "-" * 10)  # to get the current path the file is running on


# output :
# /home/yuji/Projects/public_drive/test
#  ----------
# /home/yuji/Projects/public_drive
#  ----------


os.chdir(m_path)  # change the path back to the main path

print(os.getcwd(), "\n", "-" * 10)  # to get the current path the file is running on

# os.makedirs("test/tset")

print(os.listdir(), "\n", "-" * 10)

os.removedirs("test")

print(os.listdir(), "\n", "-" * 10)
