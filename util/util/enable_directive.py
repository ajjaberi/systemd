#!/usr/bin/python3 
import os
import argparse

def parse_arguments():
    ''' Get the directive file and systemd service file as argument'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type = str, required = "True", help = "Directive file")
    parser.add_argument('-f', type = str, required = "True", help = "Systemd .service file")

    args = parser.parse_args()
    return args

def clear_lines(file):
    ''' Delete lines between to lines (start,end)'''
    start = "#Sandboxing option\n"
    end = "#End Sandboxing\n"
    source_file = open(file,"r")
    buf_source = source_file.readlines()
    source_file.close()
    dest_file = open(file,"w")
    flag = 1
    for line in buf_source:
        if line == "[Service]\n":
            line += start
        if line == start:
            flag = 0
        if line == end:
            flag = 1
        if flag == 1 and line != end:
            dest_file.write(line)
    dest_file.close()

def file_content(file):
    ''' Copy the enire file content to a buffer'''
    with open(file, "r") as source_file:
        content = source_file.readlines()
        return content

def insert_param(service_file, service_content, directives):
    with open (service_file, "w") as dest_file:
        for line in service_content:
            if line == "#Sandboxing option\n":
                for param in directives:
                    if (not param.startswith('#')):
                        line += param
                line += "#End Sandboxing\n"
            dest_file.write(line)
    dest_file.close()

def reload_service():
    ''' Reload the service after modification '''
    os.system("systemctl daemon-reload")


def main():
    args = parse_arguments()
    directive_file = args.c
    service_file = args.f
    clear_lines(service_file)
    service_content = file_content(service_file)
    directives = file_content(directive_file)
    insert_param(service_file, service_content, directives)
    reload_service()
if __name__ == "__main__":
    main()

