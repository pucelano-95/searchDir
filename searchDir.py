import os

path = "D:\\TEST\\SAFAL\\SG5.2MW-145CIIBMKII_MAKE(GF)_91m_DDBB(5.0MW_T91.4)\\"
files_and_directories = os.listdir(path)
# print (files_and_directories)

try:
    with open("D:\\TEST\\SAFAL\\foundTower.txt", "w") as sumFile:
        for file in files_and_directories:
            if file.endswith("xls"):
                sumFile.write(file + "\n")
                with open(path + file) as f:
                    for line in f:
                        if line.find("TOWER\tMY\t0") != -1:
                            sumFile.write(line + "\n")
except Exception as err:
    print("Exception:", err)
