# ++
# preprocessor_def_guard
# Copyright (c) 2018 Aidan Khoury (dude719)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# @file preprocessor_def_guard.py
# @author Aidan Khoury (dude719)
# @date 3/29/2018
# --

import os
import sys
import getopt

def usage():
    # Prints out script usage information.
    print sys.argv[0]+" [-i|--input-file=] <inputfile> [-o|--output-file=] <outputfile>"

# Preprocessor definitions to guard.
preprocessor_defs = {
    "#define STATUS_",
    "#define RPC_NT_",
    "#define DBG_"
}

def i_feel_lazy(lines,out_file):
    # Iterates each line in data searchgin for preprocessor defs,
    # and will then add a guard for each matching preprocessor def.
    i = 0
    last_line = len(lines)
    # Enumerate the entire file line by line.
    while i < last_line:
        line = lines[i]
        # If the line is too small, just skip it.
        if len(line) > 7:
            leading_ws_stripped = line.lstrip()
            comment_beginning = leading_ws_stripped[0] == '/' and leading_ws_stripped[1] == '/'
            # If it begins with a comment, skip it.
            if not comment_beginning:
                # Loop through every preprocessor def we want to guard.
                for preprocessor_def in preprocessor_defs:
                    index_begin = leading_ws_stripped.find(preprocessor_def)
                    # Did we find a line with this preprocessor def?
                    if index_begin != -1:
                        # Extract the preprocessor def name.  
                        index_end = leading_ws_stripped.find(' ',index_begin+8)
                        def_name = leading_ws_stripped[index_begin+8:index_end]
                        # Insert the preprocessor def gaurd. 
                        lines.insert(i,"#ifndef "+def_name+"\r\n")
                        lines.insert(i+2,"#endif//"+def_name+"\r\n")
                        # Adjust the last line and the current line index.
                        i += 2
                        last_line += 2
                        break  
        i += 1 # Iterate the current line index.

    # Join the new lines list.
    final_string = ''.join(lines)

    # Output to file or stdout.
    if out_file:
        try:
            f = open(out_file, "wb")
            f.write(final_string)
        finally:
            f.close()
    else:
        sys.stdout.write(final_string)

def main(argv):
    # Get options.
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["input-file=","output-file="])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    # Get the optional input and output files.  
    input_file = None
    output_file = None
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--input-file"):
            input_file = arg
        elif opt in ("-o", "--output-file"):
            output_file = arg

    # Get input.
    if input_file:
        try:
            f = open(input_file)
            lines = f.readlines()
        except:
            print("Error: failed to open file")
        finally:
            f.close() 
    else:
        print("Enter file data:")
        # Have to indicate EOF using Ctrl+Z on Windows and Crtl+D on linux.
        lines = sys.stdin.readlines() 

    # Make sure we got valid input.
    if not lines:
        print("Error: invalid input")
        sys.exit(-2)
    
    # Guard the the preprocessor defs.
    i_feel_lazy(lines, output_file)
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])