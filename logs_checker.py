#!/usr/bin/env python3

import sys 
import re 
import csv

def main(filename):
    '''
    This function try to retrieve two CSV files
    One for ERROR counts and other for counts for INFO and ERRORS for each user
    '''
    user_info = {}
    error_info = {}
    expression = r'(ERROR|INFO) : ([\w ]*).*\((\w+)\)'
    
    with open(filename,'r') as log_file:
        
        for line in log_file:
            msg = re.search(expression,line)

            if msg != None:

                index_kind = msg[1]
                index_description = msg[2]
                index_user = msg[3]
                
                user_info[index_user] = user_info.get(index_user,{'ERROR':0,'INFO':0})
                user_info[index_user][index_kind] = user_info[index_user].get(index_kind,0) + 1
                
                if 'ERROR' in line:
                    error_info[index_description] = error_info.get(index_description,0) + 1
    
    error_info = dict(sorted(error_info.items(),key=lambda x: x[1],reverse=True))
    user_info = dict(sorted(user_info.items(),key=lambda x: x[0]))
    return error_info, user_info

def write_csv(name_file_user,name_file_error, error_dict, user_dict):
    csv_error_header = ['Error','Count']
    csv_user_header = ['Username','INFO','ERROR']

    with open(name_file_error,'w') as f_error:
        writer = csv.DictWriter(f_error,fieldnames=csv_error_header)
        writer.writeheader()
        for key, values in error_dict.items():
            f_error.write(f'{key},{values}\n')
    
    with open(name_file_user,'w') as f_user:
        writer = csv.DictWriter(f_user,fieldnames=csv_user_header)
        writer.writeheader()
        for key, values in user_dict.items():
            data = {'Username':key}
            data.update(values)
            writer.writerow(data)



if __name__ == '__main__':
    error_info, user_info = main(sys.argv[1])
    write_csv('user.csv','error.csv',error_info,user_info)


