#!/usr/bin/python3
ver="2024-05-03"
######################################################
# X4_MAKLIB Ver. 2024-05-03
# (Utility for production of a new library tape.)
#
# Naohiko Otuka (IAEA Nuclear Data Section)
#  on behalf of the International Network of
#  Nuclear Reaction Data Centres (NRDC)
######################################################
import datetime
import os
import re
import argparse

def main():
  get_args(ver)
  (dir_root,lib_out,tape_id)=get_input()
  (nan,col80,area_ini,area_fin,line_out)=merge(lib_out,dir_root)

  output(lib_out,tape_id,nan,col80,area_ini,area_fin,line_out)
  
  print("")
  print("Program terminated normally.")

def output(lib_out,tape_id,nan,col80,area_ini,area_fin,line_out):
  f=open(lib_out,"w")

  n1="   {:>8s}".format(tape_id)
  time=datetime.datetime.now()
  date=time.strftime("%Y%m%d")
  n2="   {:8s}".format(date)
  n3n4n5="                                 "
  if col80==True:
    f.write("LIB        "+n1+n2+n3n4n5+area_ini+"000000000000 \n")
  else:
    f.write("LIB        "+n1+n2+"\n")

  for line in line_out:
    f.write(line)

  n1="{:>11d}".format(nan)
  n2="{:>11s}".format("0")
  if col80==True:
    f.write("ENDLIB     "+n1+"          0"+n3n4n5+area_fin+"999999999999 \n")
  else:
    f.write("ENDLIB     "+n1+"\n")

  f.close()

def merge(lib_out,dir_root):
  entries=list()
  line_out=list()
  col80=True
  dirs=os.listdir(dir_root)
  for dir in dirs:
    if os.path.isdir(dir_root+"/"+dir):
      if re.compile("^[a-zA-Z0-9]$").search(dir):
        files=os.listdir(dir_root+"/"+dir)
        for file in files:
          if re.compile(dir+"\d{4}\.txt").search(file):
            entry=dir_root+"/"+dir+"/"+file
            entries.append(entry)

  entries=sorted(entries)
  nan=len(entries)
  for i, entry in enumerate(entries):
    if args.nodic and entry.endswith("90001.txt"):
      continue
    print("adding ..."+entry)
    with open(entry) as g:
      for line in g:
        if col80==True and len(line)<80:
          col80=False
        if re.compile("^ENTRY").search(line):
          if i==0:
            area_ini=line[17:18]
          elif i==len(entries)-1:
            area_fin=line[17:18]
        if args.add19 and\
          re.compile("^(ENTRY|SUBENT|NOSUBENT)").search(line):
          if line[25:27]=="  " and line[27:33]!="      ":
            line=line[0:25]+"19"+line[27:66]
        
        line_out.append(line.rstrip()+"\n")

  return nan,col80,area_ini,area_fin,line_out


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Production of a library tape",\
          epilog="example: x4_maklib.py -d entry -l lib/library.txt -i 0001")
  parser.add_argument("-v", "--version",\
         action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-a", "--add19",\
   help="Addition of '19' to N2 ", action="store_true")
  parser.add_argument("-n", "--nodic",\
   help="Exclusion of dictionary ", action="store_true")
  parser.add_argument("-d", "--dir_root",\
   help="name of input entry storage directory")
  parser.add_argument("-l", "--lib_out",\
   help="name of output library tape")
  parser.add_argument("-i", "--tape_id",\
   help="tape ID of output")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_MAKLIB (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  dir_root=args.dir_root
  if dir_root==None:
    dir_root=input("input directory [entry] --> ")
    if dir_root=="":
      dir_root="entry"

  if not os.path.isdir(dir_root):
    print(" ** Directory '"+dir_root+"' does not exist.")
  while not os.path.isdir(dir_root):
    dir_root=input("input directory [entry] --> ")
    if dir_root=="":
      dir_root="entry"
    if not os.path.isdir(dir_root):
      print(" ** Directory '"+dir_root+"' does not exist.")

  lib_out=args.lib_out
  if lib_out==None:
    lib_out=input("output file [lib.txt] ----> ")
    if lib_out=="":
      lib_out="lib.txt"

  if os.path.isfile(lib_out):
    msg="The tape '"+lib_out+"' exists and must be deleted."
    print_error(msg,"")
    os.remove(lib_out)

  tape_id=args.tape_id
  if tape_id==None:
    tape_id=input("Tape ID of ouput [0000] --> ")
    if tape_id=="":
      tape_id="0000"

  return dir_root,lib_out,tape_id


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
