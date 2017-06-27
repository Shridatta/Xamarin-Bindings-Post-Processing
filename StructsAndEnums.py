import os
from optparse import OptionParser

def main(file_name):
    try:
        # Open Old File
        File_to_Open = open(file_name, 'r')
        File_Data = File_to_Open.readlines()
        File_to_Open.close()
        # Replace Data
        New_File_Data = []
        for i in File_Data:
            if not isinstance(i, str):
                i = i.decode("utf-8")
            if "nint" in i:
                New_File_Data.append(i.replace('nint', 'long'))
            else:
                New_File_Data.append(i)
        # Save New File
        if not os.path.exists('processed'):
            os.mkdir('processed')
        new_file_name = os.path.join('processed', file_name)
       # new_file_name = file_name[:file_name.rfind('.cs')] + "Updated.cs"
        File_to_Save = open(new_file_name, 'w+')
        for j in New_File_Data:
            File_to_Save.write(j)
        File_to_Save.close()
        print(new_file_name +" File Saved Successfully")
    except IOError:
        print("Error: File not found!")
    except:
        print("Unexpected Error!")

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file",dest="file_name", default="StructsAndEnums.cs",help="set input file name")
    (options, args) = parser.parse_args()
    main(file_name = options.file_name)