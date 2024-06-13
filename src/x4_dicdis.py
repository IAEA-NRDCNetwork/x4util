#!/usr/bin/python3
ver="2024-05-03"
######################################################
# X4_DICDIS Ver. 2024-05-03
# (Creation of dictionaries for distribution)
#
# Naohiko Otuka (IAEA Nuclear Data Section)
#  on behalf of the International Network of
#  Nuclear Reaction Data Centres (NRDC)
######################################################
from datetime import timezone
import datetime
import json
import os
import re
import argparse

def main():
  global dict_full

  dictionary_list=[
  "001",  "002", "003", "004", "005", "006", "007", "008",
  "015",  "016", "017", "018", "019",
  "020",  "021", "022", "023", "024", "025", "026",
  "030",  "031", "032", "033", "034", "035", "037", "038",
  "043",  "045", "047", "048", 
  "052", 
  "113",  "144",
  "207",  "209", "213", "227", "235", "236"]

  time=datetime.datetime.now(timezone.utc)
  date_out=time.strftime("%Y%m")

  get_args(ver)
  (dict_ver,dir_input,dir_output)=get_input()


# Read JSON Dictionary
  file_in=dir_input+"/dict."+dict_ver+".json"
  if os.path.exists(file_in):
    f=open(file_in, 'r')
    dict_full=json.load(f)
    f.close()
  else:
    msg="File "+file_in+" does not exist."
    line=""
    print_error_fatal(msg,line)

  for dict_id in list(dictionary_list):
    for key in list(dict_full[dict_id]):
      if key!="comment":
        alteration_flag=dict_full[dict_id][key]["alteration_flag"]
        if alteration_flag=="D":
          dict_full[dict_id].pop(key)
        elif alteration_flag=="A" or\
             alteration_flag=="S" or\
             alteration_flag=="M":
          dict_full[dict_id][key]["date"]=date_out
          dict_full[dict_id][key]["alteration_flag"]=" "

# Produce JSON Dictionary for distribution
  json_out=json.dumps(dict_full,indent=2)
  file_out=dir_output+"/dict."+dict_ver+".json"
  print("printing JSON dictionary    ... ")
  f=open(file_out,'w')
  f.write(json_out)
  f.close()


# Produce Archive Dictionary
  print("printing Archive dictionary ... ", end="")
  print_archive(dir_input,dir_output,date_out,dictionary_list)


# Produce Backup Dictionary
  archive_to_backup(dir_output,dict_ver,dictionary_list)

  print("Conversion completed. Good bye!")


# Print Archive Dictionary after updating/excluding flagged records
def print_archive(dir_input,dir_output,date_out,dictionary_list):
  file_in=dir_input+"/dict_arc.top"
  lines=get_file_lines(file_in)
  file_out=dir_output+"/dict_arc.top"
  print("top", end=", ")
  f=open(file_out,'w')

  for line in lines:
    f.write(line+"\n")
  f.close()

  for dict_id in dictionary_list:
    if re.compile("a$").search(dict_id):
      continue
    print(dict_id, end=" ")
    file_in=dir_input+"/dict_arc_new."+dict_id
    lines=get_file_lines(file_in)
    file_out=dir_output+"/dict_arc_new."+dict_id
    f=open(file_out,'w')
    out="y"
    for line in lines:
      alteration_flag=line[0:1]
      date=line[5:11]
      key=line[12:42]
      if re.compile("\S+").search(key):
        if  alteration_flag=="D":
          out="n"
        else:
          out="y"
          if alteration_flag=="A" or\
             alteration_flag=="S" or\
             alteration_flag=="M":
            line=line.replace(date,date_out)
      if out=="y":
        line=" "+line[1:123]
        f.write(line+"\n")
    f.close()
  print()
  print()


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Prepare Archive, Backup and JSON Dictionaries for distribution",\
          epilog="example: x4_dicdis.py -n 9128 -i input -o output")
  parser.add_argument("-v", "--version",\
         action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-n", "--dict_ver",\
   help="dictionary version (transmission ID)")
  parser.add_argument("-i", "--dir_input",\
   help="name of input Archive and JSON Dictionary directory")
  parser.add_argument("-o", "--dir_output",\
   help="name of output Archive/Backup/JSON Dictionary directory")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_DICDIS (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  dict_ver=args.dict_ver
  if dict_ver==None:
    dict_ver=input("input dictionary TRANS ID [9128] -------------------> ")
    if dict_ver=="":
      dict_ver="9128"
  if not re.compile("^\d{4,4}$").search(dict_ver):
    print(" ** Dictionary version must be four-digit integer.")
  while not re.compile("^\d{4,4}$").search(dict_ver):
    dict_ver=input("input dictionary TRANS ID [9128] -------------------> ")
    if dict_ver=="":
      dict_ver="9128"
    if not re.compile("^\d{4,4}$").search(dict_ver):
      print(" ** Dictionary version must be four-digit integer.")

  dir_input=args.dir_input
  if dir_input==None:
    dir_input=input("input Archive+JSON dictionary dictionaries [input] -> ")
    if dir_input=="":
      dir_input="input"
  if not os.path.exists(dir_input):
    print(" ** Folder "+dir_input+" does not exist.")
  while not os.path.exists(dir_input):
    dir_input=input("input Archive+JSON dictionary dictionaries [input] -> ")
    if dir_input=="":
      dir_input="input"
    if not os.path.exists(dir_input):
      print(" ** Folder "+dir_input+" does not exist.")

  dir_output=args.dir_output
  if dir_output==None:
    dir_output=input("output Archive+Backup+JSON directory [dist] --------> ")
  if dir_output=="":
    dir_output="dist";
  if not os.path.isdir(dir_output):
    msg="Directionry '"+dir_output+"' does not exist and must be created."
    print_error(msg,"")
    os.mkdir(dir_output)
  if os.path.isfile(dir_output):
    msg="Directory '"+dir_output+"' exists and must be overwritten."
    print_error(msg,"")

  return dict_ver,dir_input,dir_output


def archive_to_backup(dir_output,dict_ver,dictionary_list):
  nline=dict()
  for dict_id in dictionary_list:
    if re.compile("a$").search(dict_id):
      continue
    num="%3s" % int(dict_id)
    file_in=dir_output+"/dict_arc_new."+dict_id
    lines=get_file_lines(file_in)
    nline[num]=0
    for line in lines:
      if re.compile("\S+").search(line[12:42]):
        nline[num]+=1

  file_out=dir_output+"/dan_back_new."+dict_ver
  print("printing backup dictionary  ... ")
  g=open(file_out,"w")
  lines=get_file_lines(dir_output+"/dict_arc.top")
  for line in lines:
    num=line[0:3]
    line=line[0:83]+"%4s" % nline[num]
    print(line,file=g)
  print("",file=g)
  for dict_id in dictionary_list:
    if re.compile("a$").search(dict_id):
      continue
    num="%3s" % int(dict_id)
    file_in=dir_output+"/dict_arc_new."+dict_id
    lines=get_file_lines(file_in)
    for line in lines:
      if dict_id=="001":
        line=line.replace(line[53:108]," "*55)
      elif dict_id=="025":
        line=line[0:93]+"   "+line[96:123]
      if re.compile("\S+").search(line[12:42]):
        print(num+line,file=g)
  g.close()


def get_file_lines(file):
  if os.path.exists(file):
    f=open(file, 'r')
    lines=f.read().splitlines()
    f.close()
  else:
    msg="File "+file+" does not exist."
    line=""
    print_error_fatal(msg,line)
  return lines

def print_error_fatal(msg,line):
  print("** "+msg)
  print(line)
  exit()


def print_error(msg,line):
  print("** "+msg)
  print(line)

  if args.force:
    answer="Y"
  else:
    answer=""

  while answer!="Y" and answer!="N":
    answer=input("Continue? [Y] --> ")
    if answer=="":
      answer="Y"
    if answer!="Y" and answer!="N":
      print(" ** Answer must be Y (Yes) or N (No).")
  if answer=="N":
    print("program terminated")
    exit()


if __name__ == "__main__":
  dict_full=dict()

  main()
  exit()
