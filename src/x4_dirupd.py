#!/usr/bin/python3
ver="2024-05-03"
######################################################
# X4_DIRUPD Ver. 2024-05-03
# (Utility to update EXFOR entry local storage)
#
# Naohiko Otuka (IAEA Nuclear Data Section)
#  on behalf of the International network of
#  Nuclear Reaction Data Centres (NRDC)
######################################################
import datetime
import os
import re
import shutil
import argparse

def main():
  get_args(ver)
  (trans_in,dir_root)=get_input()
  (dict,tid_new,tdate_new)=check_dict(trans_in)

  if dict==True:
    dir_out=dir_root+"/9/"
    if not os.path.isdir(dir_out):
      os.mkdir(dir_out)
    dict_out=dir_out+"90001.txt"
    write_dict(tid_new,trans_in,dict_out)
    update_log(tid_new,tdate_new,trans_in)
    print("")
    print("Program terminated normally.")
  else:
    (ok,file_lst)=analyse(trans_in,dir_root,tid_new)
   
    if ok==0:
      print("")
      print("Program terminated abnormally. ENDTRANS absent")
    else:
      write_exfor(file_lst,dir_root)
      update_log(tid_new,tdate_new,trans_in)
      print("")
      print("Program terminated normally.")


def write_dict(tid_new,trans_in,dict_out):
  f=open(dict_out,'w',encoding='iso-8859-1')
  g=open(trans_in,'r',encoding='iso-8859-1')
  if os.path.isfile(dict_out):
     print("updating ..."+dict_out)
  else:
     print("adding ..."+dict_out)
  with open(dict_out,"w") as f:
    with open(trans_in) as g:
      for line in g:
        if line[0:10]=="TRANS     " or line[0:10]=="ENDTRANS  ":
          continue

        if line[0:10]=="DICTION   ":
          n3n4="                      "
          char1=line[:10]    # keyword ("DICTION   ")
          char2=line[11:33]  # entry number and date (N1+N2)
          char3=line[66:79]  # line sequential number
          line=char1+" "+char2+n3n4+"       "+tid_new+char3+" \n"

        if args.cut66:
          line=line[0:66].rstrip()
          if re.compile("^ENDDICTION").search(line):
            line=line[0:22] # Delete N2=0
          line=line+"\n"

        f.write(line)

    g.close()
  f.close()



def check_dict(trans_in):
  g=open(trans_in,'r',encoding='iso-8859-1')
  for i,line_new in enumerate(g): # loop for lines in TRANS tape
    if i==0: # first record must be TRANS
      tdate_new=line_new[25:33]
      if line_new[0:10]!="TRANS     ":
        msg="The first record must be TRANS."
        print_error_fatal(msg,line_new)
      else:
        tid_new=line_new[18:22]
        check_tid_new(tid_new)
        if line_new[18:19]=="9":
          dict=True
        else:
          dict=False
        return dict,tid_new,tdate_new

# Analyse an existing entry file if exists
def analyse(trans_in,dir_root,tid_new):
  ok=0
  n3n4="                      "
  g=open(trans_in,'r',encoding='iso-8859-1')

  for i,line_new in enumerate(g): # loop for lines in TRANS tape

    if line_new[0:10]=="TRANS     ":
      file_lst=list()

    elif line_new[0:10]=="ENDTRANS  ":
      ok=1
      return ok,file_lst

    elif line_new[0:10]=="ENTRY     ":
      line_out=dict() # lines for addition to new entry file
      stat=dict()     # status of subentry (new/udpate/not update)
      tid_old=dict()  # ENTRY/SUBENT/NOSUBENT TID of existing entry file
      date_old=dict() # ENTRY/SUBENT/NOSUBENT N2 of existing entry file
      date_new=dict() # ENTRY/SBUENT/NOSUBENT N2 in Trans

      area=line_new[17:18].lower()
      dir_out=dir_root+"/"+area
      if not os.path.isdir(dir_out):
        os.mkdir(dir_out)

      altflag=line_new[10:11]
      an=line_new[17:22]
      san=an+".000"

      date_new[san]=line_new[25:33]

      char1=line_new[:10]    # keyword ("ENTRY     ")
      char2=line_new[11:33]  # entry number and date (N1+N2)
      char3=line_new[66:79]  # line sequential number
      line_out[san]=[char1+" "+char2+n3n4+"       "+tid_new+char3+" \n"]

      exfor_old=dir_out+"/"+an.lower()+".txt"
      if os.path.isfile(exfor_old): # this entry is in the storage
        f=open(exfor_old,'r')

        for i,line_old in enumerate(f): # loop for lines in the storage
          if i==0: # first trecord must be ENTRY
            if line_old[0:10]!="ENTRY     ":
              msg=exfor_old+": The first record must be ENTRY."
              print_error_fatal(msg,line_old)
         
          if line_old[0:10]=="ENTRY     ":
            if line_old[17:22]!=an:
              msg="File "+exfor_old+" is not for entry "+an
              print_error_fatal(msg,line_old)
            san=an+".000" # special subentry number for the ENTRY ercord
            stat[san]="(for alteration)"
            date_old[san]=line_old[25:33] # entry date (ENTRY N2)
            tid_old[san]=line_old[62:66]  # entry Trans ID (ENTRY N5)
         
          elif line_old[0:10]=="SUBENT    " or\
               line_old[0:10]=="NOSUBENT  ":

# add 19 to 2-digit year (for comparison with VZ's backup)
#           if args.add19 and line_old[25:27]=="  ": # 2-digit to 4-digit year
#             line_old=line_old[0:25]+"19"+line_old[27:66]

            san=an+"."+line_old[19:22]
            stat[san]="(not for alteration)"
            date_old[san]=line_old[25:33]# subentry date (SUBENT N2)
            tid_old[san]=line_old[62:66] # subentry Trans ID (SUBENT N5)
            line_out[san]=[line_old]     # SUBENT record in storage
                                         # (will be altered if needed)
         
          elif line_old[0:10]=="ENDENTRY  ":
            pass
         
          else:
            line_out[san].append(line_old)

        f.close()

      san=an+".000"
      if altflag==" ":
        if san in stat: # The entry is in storage. Anyway update?
          msg="Entry "+an+" is in storage but alt. flag C is absent."
          print_error(msg,line_new)
        else:
          stat[san]="(for creation)"
      
      elif altflag=="C":
        if not san in stat: # The entry not in storage. Anyway create?
          msg="Entry "+an+" is not in storage but alt. flag C is present."
          print_error(msg,line_new)
          stat[san]="(for creation)"

      print("analysing ... "+an+" "+stat[san])


    elif line_new[0:10]=="SUBENT    ":

      altflag=line_new[10:11]
      san=an+"."+line_new[19:22]

      if altflag==" " or altflag=="I":
        if san in stat: # The subentry is in storage. Anyway update?
          msg="Subentry "+san+" is in storage but alt. flag C is absent."
          print_error(msg,line_new)
          stat[san]="(for alteration)"
        else:
          stat[san]="(for creation)"

      elif altflag=="C": # The subentry not in storage. Anyway create?
        if not san in stat:
          msg="Subentry "+san+" is not in storage but alt. flag C is present."
          print_error(msg,line_new)
          stat[san]="(for creation)"
        else:
          stat[san]="(for alteration)"

      print("analysing ... "+san+" "+stat[san])

      date_new[san]=line_new[25:33] #subentry date (SUBENT N2)

      char1=line_new[:10]           #keyword ("SUBENT    ")
      char2=line_new[11:33]         #subentry number+date (SUBENT N2+N3)
      char3=line_new[66:79]         #line sequential number
      line_out[san]=[char1+" "+char2+n3n4+"       "+tid_new+char3+" \n"]

    elif line_new[0:10]=="NOSUBENT  ":

      altflag=line_new[10:11]
      san=an+"."+line_new[19:22]

      if altflag!=" ":
        msg="Subentry "+san+" is in storage but alt. flag C is absent."
        print_error(msg,line_new)

      if san in stat:
        stat[san]="(for deletion)"
      else:
        stat[san]="(for creation)"

      print("analysing ... "+san+" "+stat[san])
      date_new[san]=line_new[25:33]#subentry date (NOSUBENT N2)

      char1=line_new[:10]          #keyword ("NOSUBENT  ")
      char2=line_new[11:33]        #subentry number+date(NOSUBENT N2+N3)
      char3=line_new[66:79]        #line seuqnetial number
      line_out[san]=[char1+" "+char2+n3n4+"       "+tid_new+char3+" \n"]

    elif line_new[0:10]=="ENDENTRY  ":
      san=an+".999"
      stat[san]=""

      san_list=sorted(list(stat.keys())) #list of subentry numbers incl.
      nsan=len(san_list)-2               #ENTRY (000) and ENDENTRY (999)

      char1=line_new[:10]          # keyword ("ENDENTRY    ")
      char2="{:>11d}".format(nsan) # Number of subentries (N1)
      char3=line_new[22:33]        # 0 or empty (ENDENTRY N2)
      char4="                                 " # N3+N4+N5 (empty)
      char5=line_new[66:79]        # line sequential number
      line_out[san]=[char1+" "+char2+char3+char4+char5+" \n"]

      for san in san_list:
        if stat[san]=="(for alteration)":
          check_order(san,date_old[san],date_new[san],tid_old[san],tid_new)
      exfor_new=an.lower()+".txt"

      f=open(exfor_new,'w')
      for san in san_list:
        for line in line_out[san]:

          if args.cut66:
            line=line[0:66].rstrip()
            if re.compile("^END(BIB|COMMON|DATA|SUBENT|ENTRY)").search(line):
              line=line[0:22] # Delete N2=0
            line=line+"\n"

          f.write(line)
      f.close()
      file_lst.append(exfor_new)

    else:
      line_out[san].append(line_new[0:79]+" \n")

  return ok,tid_new,file_lst


def write_exfor(file_lst,dir_root):
  if args.force:
    answer="Y"
  else:
    answer=""

  while answer!="Y" and answer!="N":
    answer=input("Analysis completed. Overwrite storage? [N] --> ")
    if answer=="":
      answer="N"
    if answer!="Y" and answer!="N":
      print(" ** Answer must be Y (Yes) or N (No).")

  for exfor_new in file_lst:
    area=exfor_new[0:1].lower()
    exfor_old=dir_root+"/"+area+"/"+exfor_new

    if answer=="Y":
      print("writing to storage... "+exfor_new)
      shutil.move(exfor_new, exfor_old)

    else:
      print("deleting ... "+exfor_new)
      os.remove(exfor_new)


def update_log(tid_new,tdate_new,trans_in):
  centre={'1': 'NNDC  ',  '2': 'NEADB ', '3': 'NDS   ',  '4': 'CJD   ',
          '9': 'NDS   ',
          'A': 'CNPD  ',  'B': 'NDS   ', 'C': 'NNDC  ',  'D': 'NDS   ',
          'E': 'JCPRG ',  'F': 'CNPD  ', 'G': 'NDS   ',  'J': 'JCPRG ',
          'K': 'JCPRG ',  'L': 'NNDC  ', 'M': 'CDFE  ',  'O': 'NEADB ',
          'R': 'JCPRG ',  'S': 'CNDC  ', 'V': 'NDS   '}

  area=tid_new[0:1]
  if area in centre:
    centre_out=centre[area]
  else:
    msg="Unexpected area character in TRANS ID: "+area
    print_error_fatal(msg,"")
  
  seq=-1
  if os.path.isfile("dirupd.log"):
    with open("dirupd.log") as f:
      for line in f:
        seq+=1
  else:
    msg="dirupd.log is missing."
    print_error_fatal(msg,"")
  seq='{:>4}'.format(seq)

  time=datetime.datetime.now()
  stamp=time.strftime("%Y-%m-%d %H:%M:%S.%f")
  line=seq+" "+stamp+" "+tid_new+"      "+tdate_new+"   "+centre_out+" "+trans_in+"\n"  
  f=open("dirupd.log",'a')
  f.write(line)
  f.close() 


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Update of an EXFOR entry local storage",
          epilog="example: x4_dirupd.py -t trans/trans.txt -d entry")
  parser.add_argument("-v", "--version",\
          action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-c", "--cut66",\
   help="delete cols.67-80 and trailing blanks before col.67", action="store_true")
  parser.add_argument("-t", "--trans_in",\
   help="name of input trans tape")
  parser.add_argument("-d", "--dir_root",\
   help="name of output entry storage directory")

# parser.add_argument("-u", "--updN2",\
#  help="set N2 of ENTRY to N2 of SUBENT 001", action="store_true")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_DIRUPD (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  trans_in=args.trans_in
  if trans_in==None:
    trans_in=input("input file [trans/trans.txt] --> ")
    if trans_in=="":
      trans_in="trans/trans.txt"
  if not os.path.exists(trans_in):
    print(" ** File '"+trans_in+"' does not exist.")
  while not os.path.exists(trans_in):
    trans_in=input("input file [trans/trans.txt] --> ")
    if trans_in=="":
      trans_in="trans/trans.txt"
    if not os.path.exists(trans_in):
      print(" ** File '"+trans_in+"' does not exist.")

  dir_root=args.dir_root
  if dir_root==None:
    dir_root=input("output directory [entry] ------> ")
    if dir_root=="":
      dir_root="entry"

  if not os.path.isdir(dir_root):
    print(" ** Directory '"+dir_root+"' does not exist.")
  while not os.path.isdir(dir_root):
    dir_root=input("output directory [entry] ------> ")
    if dir_root=="":
      dir_root="entry"
    if not os.path.isdir(dir_root):
      print(" ** Directory '"+dir_root+"' does not exist.")

  return trans_in,dir_root


def check_order(san,date_old,date_new,tid_old,tid_new):
  msg=""

  if date_old>date_new:
    msg=san+": date in storage ("+date_old+\
     ") >    date in trans ("+date_new+")"
    print_error(msg,"")

  elif date_old==date_new:
    msg=san+": date in storage ("+date_old+\
     ") =    date in trans ("+date_new+")"
    print_error(msg,"")

  if not re.compile("^Y").search(tid_old):
    if tid_old[0:1]!=tid_new[0:1] and tid_old[0:1]!="0":
      msg=san+": tape ID in storage ("+tid_old+\
       ")  and tape ID in new trans ("+tid_new+") from different areas"
      print_error(msg,"")

    elif tid_old>tid_new:
      msg=san+": tape ID in storage ("+tid_old+\
      ")  >    tape ID in trans ("+tid_new+")"
      print_error(msg,"")

    elif tid_old==tid_new:
      msg=san+": tape ID in storage ("+tid_old+\
      ")  =    tape ID in trans ("+tid_new+")"
      print_error(msg,"")


def check_tid_new(tid_new):

  ok=0
  tid_num=0
  area=tid_new[0:1]
  tid_new_num=int(re.sub("^0+","",tid_new[1:4]))

  l=open("dirupd.log",'r')
  s=l.readlines()
  l.close()
  for line in s:
    if line[0:4]=="   0":
      continue
    if line[32:33]!=area:
      continue
    line_out=line

    tid=line[33:36]
    tid_num=int(re.sub("^0+","",tid))

  if tid_num==0:
    ok=1
  else:
    if tid_new_num==tid_num+1:
      ok=1
    elif tid_new_num==tid_num:
      ok=2
    else:
      ok=0

  if ok==2:
    msg="The log file indicates "+tid_new+" is same as the one loaded last time for this area: \n     "+line_out
    print_error(msg,"")
  
  elif ok==0:
    msg="The log file indicates "+tid_new+" is inconsistent with the one loaded last time for this area: \n     "+line_out
    print_error(msg,"")


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
