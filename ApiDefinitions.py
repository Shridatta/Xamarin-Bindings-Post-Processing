import os
from optparse import OptionParser

def check_str(input_data):
    if not isinstance(input_data, str):
        return input_data.decode("utf-8")
    else:
        return input_data

def main(file_name):
    try:
        # Open Old File
        File_to_Open = open(file_name, 'r')
        File_Data = File_to_Open.readlines()
        File_to_Open.close()
        # Replace Data
        New_File_Data = []
        Current_Data = ""
        Next_Data = ""
        Later_Data = ""
        is_opened = False
        i = 0
        while i < len(File_Data):
            Current_Data = check_str(File_Data[i])
            try:
                Next_Data = check_str(File_Data[i+1])
            except:
                Next_Data = ""
            if "unsafe" in Current_Data:
                Current_Data = Current_Data.replace('unsafe ', '')
            if "sbyte*" in Current_Data:
                Current_Data = Current_Data.replace('sbyte*', '[PlainString]string')
            if "GetType()" in Current_Data:
                Current_Data = Current_Data.replace('GetType()', 'GetTypeXamarin()')
            if "void*" in Current_Data:
                Current_Data = Current_Data.replace('void*', 'ref IntPtr')
                if "(" in Current_Data and Current_Data.index("(")>Current_Data.index("ref IntPtr"):
                    Current_Data = Current_Data.replace('ref IntPtr', 'IntPtr',1)
            if "[Export" in Current_Data and "[Verify (MethodToProperty)]" in Next_Data:
                i += 1
                Next_Data = check_str(File_Data[i+1])
                File_Data[i+1] = "\t\t" + " ".join(Next_Data.split()[:Next_Data.split().index("{") - 1]) + " " + Current_Data[Current_Data.find('"')+1:Current_Data.rfind('"')] + "();\n"
            if "[Protocol, Model]" in Current_Data:
                Current_Data = "\t[BaseType(typeof(NSObject))]\n" + Current_Data
                Later_Data = Next_Data.replace('\n','') + " {}\n"
                is_opened = True
                File_Data[i+1] = "\t" + " ".join([Next_Data.split()[0],Next_Data.split()[1].replace('I', '',1)]) + "\n"
            if Current_Data.split() == ["}"] and is_opened == True:
                is_opened = False
                Current_Data += Later_Data
            New_File_Data.append(Current_Data)
            i += 1
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
    parser.add_option("-f", "--file",dest="file_name", default="ApiDefinitions.cs",help="set input file name")
    (options, args) = parser.parse_args()
    main(file_name = options.file_name)