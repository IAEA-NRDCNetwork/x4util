#!/usr/bin/python3
ver="2023-05-03"
######################################################
# X4_DIRINI Ver. 2023-05-03
# (Utility to initialize EXFOR entry local storage)
#
# Naohiko Otuka (IAEA Nuclear Data Section)
#  on behalf of the International Network of
#  Nuclear Reaction Data Centres (NRDC)
######################################################
import datetime
import os
import re
import shutil
import argparse

def main():
  get_args(ver)
  (lib_in,dir_root)=get_input()
  clean(dir_root)
  (ok,tid_new,tdate_new)=split(lib_in,dir_root)
 
  if ok==0:
    msg="Program terminated abnormally. Proper END record is absent"
    print_error_fatal(msg,line)
  else:
    update_log(tid_new,tdate_new,lib_in)
    print("")
    print("Program terminated normally.")

# delete directory having single character name
def clean(dir_root):
  files=os.listdir(dir_root)
  for file in files:
    if os.path.isdir(dir_root+"/"+file):
      if re.compile("^[a-zA-Z0-9]$").search(file):
        print("Directory "+dir_root+"/"+file+" deleted")
        shutil.rmtree(dir_root+"/"+file)


# extraction of each entry and its output to *.txt
def split(lib_in,dir_root):

  ok=0
  sec=""
  g=open(lib_in,'r',encoding='iso-8859-1')

  for i,line in enumerate(g):

    if args.cut66:
      if len(line)>79:
        line=line[0:66].rstrip()
        line=line.rstrip()
        line=line+"\n"
      
      if re.compile("^END(BIB|COMMON|DATA|SUBENT|ENTRY|DICT)").search(line):
        line=line[0:22]+"\n" # Delete N2=0

    key=line[0:10]
    if i==0: # first record must be REQUEST or LIB
      if key!="REQUEST   " and key!="LIB       " and\
         key!="MASTER    " and key!="BACKUP    ":
        msg="The first record must be REQUEST or LIB."
        print_error_fatal(msg,line)

    if key=="REQUEST   " and sec!="DIC":
      tid_new=line[18:22]
      tdate_new=line[25:33]

    elif key=="ENDREQUEST" and sec!="DIC":
      ok=1
      return ok, tid_new, tdate_new

    elif key=="LIB       " and sec!="DIC":
      tid_new=line[18:22]
      tdate_new=line[25:33]

    elif key=="ENDLIB    " and sec!="DIC":
      ok=1
      return ok, tid_new, tdate_new

    elif key=="MASTER    " and sec!="DIC":
      tid_new=line[18:22]
      tdate_new=line[25:33]

    elif key=="ENDMASTER " and sec!="DIC":
      ok=1
      return ok, tid_new, tdate_new

    elif key=="BACKUP    " and sec!="DIC":
      tid_new=line[18:22]
      tdate_new=line[25:33]

    elif key=="ENDBACKUP " and sec!="DIC":
      ok=1
      return ok, tid_new, tdate_new

    elif key=="ENTRY     " and sec!="DIC":
      sec="ENT"
      area=line[17:18].lower()
      dir_out=dir_root+"/"+area 
      if not (os.path.isdir(dir_out)):
        os.mkdir(dir_out)

      an=line[17:22].lower()
      exfor_out=dir_out+"/"+an+".txt"
      f=open(exfor_out,'w')
      print("creating ... "+exfor_out)

      line=line[0:33]+"                      "+line[55:]
      f.write(line)

    elif key=="ENDENTRY  " and sec!="DIC":
      sec="   "
      f.write(line)
      f.close()

    elif key=="DICTION   ":
      sec="DIC"
      dir_out=dir_root+"/9"
      if not (os.path.isdir(dir_out)):
        os.mkdir(dir_out)

      an=line[17:22].lower()
      exfor_out=dir_out+"/90001.txt"

      if line[32:33]=="1":
        f=open(exfor_out,'w')
        print("creating ... "+exfor_out)
      else:
        f=open(exfor_out,'a')

      line=line[0:33]+"                      "+line[55:]
      f.write(line)

    elif key=="ENDDICTION":
      sec="   "
      f.write(line)
      f.close()

    elif key=="SUBENT    " and sec!="DIC":
      line=line[0:33]+"                      "+line[55:]
      f.write(line)

    elif key=="NOSUBENT  " and sec!="DIC":
      line=line[0:33]+"                      "+line[55:]
      f.write(line)

    elif sec=="ENT" or sec=="DIC":
      f.write(line)

    else:
      msg="Unexpected line found."
      print_error_fatal(msg,line)

  msg="Unexpected last line found."
  print_error_fatal(msg,line)


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Initialize an EXFOR entry local storage",\
          epilog="example: x4_dirini.py -l lib/library.txt -d entry")
  parser.add_argument("-v", "--version",\
         action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-c", "--cut66",\
   help="delete cols.67-80 and trailing blanks before col.67", action="store_true")
  parser.add_argument("-l", "--lib_in",\
   help="name of input library file")
  parser.add_argument("-d", "--dir_root",\
   help="name of output entry storage directory")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_DIRINI (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  lib_in=args.lib_in
  if lib_in==None:
    lib_in=input("input library file [lib/lib.txt] --> ")
    if lib_in=="":
      lib_in="lib/lib.txt"
  if not os.path.exists(lib_in):
    print(" ** File '"+lib_in+"' does not exist.")
  while not os.path.exists(lib_in):
    lib_in=input("input library file [lib/lib.txt] --> ")
    if lib_in=="":
      lib_in="lib/lib.txt"
    if not os.path.exists(lib_in):
      print(" ** File '"+lib_in+"' does not exist.")

  dir_root=args.dir_root
  if dir_root==None:
    dir_root=input("output directory [entry] ----------> ")
    if dir_root=="":
      dir_root="entry"

  if os.path.isdir(dir_root):
    msg="Directory '"+dir_root+"' exists and must be initialised."
    print_error(msg,"")
  else:
    msg="Directory '"+dir_root+"' does not exist and must be created."
    print_error(msg,"")
    os.mkdir(dir_root)

  return lib_in,dir_root


def update_log(tid_new,tdate_new,lib_in):
  f=open("dirupd.log",'w')
  line="Seq. Update date/time           Trans(N1) Trans(N2)  Centre Tape\n"
  f.write(line)
  time=datetime.datetime.now()
  stamp=time.strftime("%Y-%m-%d %H:%M:%S.%f")
  line="   0 "+stamp+" "+tid_new+"      "+tdate_new+"          "+lib_in+"\n"  
  f.write(line)
  f.close()


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
  main()
  exit()
