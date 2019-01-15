from subprocess import call
import sys
import re
import os


def generate_c_code(objects, return_type):

    c_code = "#include<stdio.h>\n#include<string.h>\n#include<unistd.h>\n#include<sys/mman.h>\n\n"

    char_array = "char code[] = {"

    for hex_ in objects:
        char_array+=(hex_+",")
    
    char_array = char_array[:-1]
    char_array += "};\n\n"

    c_code +=char_array;

    c_code += "int main(int argc, char **argv){\n\n";

    c_code += "\tvoid *buffer = mmap (0,sizeof(code),PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON,-1,0);\n"
    c_code += "\tmemcpy (buffer, code, sizeof(code));\n"
    c_code += "\t"+return_type + " value = (("+return_type+" (*) (void))buffer)();\n"

    c_code += "\t/*Modify from here, to handle return value : */\n\n\n"

    c_code += "\treturn 0;\n"
    c_code += "}\n"

    open('Generated.c', "w").write(c_code)



def generate_out(filename) :

    if not os.path.exists(filename) :
        print("Cannot find file "+filename)
        return
    
    call(['gcc', '-nostdlib', filename])
    call(['objdump', '-d', 'a.out'], stdout = open('temp.txt', 'w'))

def code_parser() :

    file_data = open('temp.txt').readlines()

    object_codes = []

    for line in file_data:
        if line == '\n' :
            continue
        object_codes.append(line.strip())
    #remove header information:
    object_codes = object_codes[3:]

    #obtain only object codes: 
    objects = []
    for line in object_codes:
        codes = line.split("\t")[1].strip().split(" ")
        
        for code in codes :
            objects.append('0x'+code)
    
    objects.append('0x00');

    return objects
    


def main() :

    filename = sys.argv[1]
    ret_type = sys.argv[2]
    generate_out(filename)
    objects = code_parser()
    generate_c_code(objects, ret_type)

main()
