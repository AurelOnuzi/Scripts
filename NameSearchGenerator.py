#!/usr/bin/env python3
#Aurel Onuzi

import csv
import os.path
import sys

#user input
names_file = input('Enter a text file with a list of name: ')
nickname_file = input('Enter a file with a list of nicknames, or just enter 0 to skip this step: ')
name_var = input('Select name variation: Single Line or Multiple Lines ( either enter single(or type 0) or enter multiple(or type 1) ): ')

#dictionary where firstname is the key and nicknames are the values, 1:N pair
nickname_dict = {}

#some  error handling with file names
if not os.path.isfile(names_file):
    raise SystemError('No file found')

if not names_file.endswith('.txt'):
    names_file = names_file+'.txt'

if not nickname_file.endswith('.txt'):
    nickname_file = nickname_file+'.txt'

if name_var.strip().lower() == 'single':
    name_var = '0'
elif name_var.strip().lower() == 'multiple':
    name_var = '1'
elif name_var.strip() != '0' and name_var.strip() != '1':
    raise SystemError('Wrong selection was given')

def name_variations(first,last):
    if name_var == '0':
        print('(',end="")
        nickname_single_variations(first,last)
        print(')',end="")
    if name_var == '1':
        nickname_multi_variations(first,last)

def generate_single_var(first,last):
    print('{0} {1} OR {1}, {0} OR {2}{0} OR {0} w/2 {1}'.format(first, last, last[:1]), end="")
    #third variation generates first initial of last name followed by the first name similar to the example
    #if you meant the first initial of the first name followed by the last name, change it to the line below
    #print('{0} {1} OR {1}, {0} OR {2}{1} OR {0} w/2 {1}'.format(first, last, first[:1]), end="")

def generate_multi_var(first,last):
    print('{0} {1}\n{1}, {0}\n{2}{0}\n{0} w/2 {1}'.format(first, last, first[:1]))

def populate_dict(file):
    #creating a dictionary with first names as key to nicknames as values
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            if row: #ignoring blank lines
                if row[0] in nickname_dict:
                    nickname_dict[row[0]].append(row[1])
                elif row:
                    nickname_dict[row[0]] = [row[1]]

def nickname_single_variations(firstname,last):
    # initial name variation
    generate_single_var(firstname,last)

    #nickname variations
    for key, val in nickname_dict.items():
        if  key == firstname:
            for val in nickname_dict[key]:
                print(' OR ',end="")
                generate_single_var(val,last)

def nickname_multi_variations(firstname,last):
    generate_multi_var(firstname,last)

    for key, val in nickname_dict.items():
        if  key == firstname:
            for val in nickname_dict[key]:
                generate_multi_var(val,last)

def main():
    if not nickname_file == '0': #nicknames file available
        populate_dict(nickname_file)

    base_file =  os.path.basename(names_file)
    new_file = os.path.splitext(base_file)[0] + '_Search.txt'
    origal_stdout = sys.stdout #for reverting back to original standard output

    with open(names_file,'r') as input_file, open(new_file,'w') as  output_file:
        sys.stdout = output_file #sending data from standard output to the file instead
        for line in input_file:
            name = line.split()
            name_variations(name[0],name[1])
        sys.stdout = origal_stdout

if __name__ == "__main__":
    main()