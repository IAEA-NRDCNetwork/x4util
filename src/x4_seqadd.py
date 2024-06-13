#!/usr/bin/python3
ver="2024-05-03"
######################################################
# X4_SEQADD Ver. 2024-05-03
# (Utility for addition of record identification etc.)
#
# Naohiko Otuka (IAEA Nuclear Data Section)
#  on behalf of the International Network of
#  Nuclear Reaction Data Centres (NRDC)
######################################################
import datetime
import os
import re
import argparse

nsan=dict() # number of subentries
nrec=dict() # number of records in the subentry
nbib=dict() # number of records in BIB section
nkey=dict() # number of keywords in BIB section
ncom=dict() # number of records in COMMON section
mcom=dict() # number of data fields in COMMON section
ndat=dict() # number of records in DATA section
mdat=dict() # number of data fields in DATA section
nlin=dict() # number of data lines in DATA section

def main():
  get_args(ver)
  (tape_in,tape_out)=get_input()
  (nan, nsan, nrec, nbib, nkey, ncom, mcom, ndat, mdat, nlin)=count(tape_in)
  output(tape_in, tape_out, nan, nsan, nrec, nbib, nkey, ncom, mcom, ndat, mdat, nlin)

  print("")
  print("Program terminated normally.")


def output(tape_in, tape_out, nan, nsan, nrec, nbib, nkey, ncom, mcom, ndat, mdat, nlin):

  n3n4n5= "                                 "
  n3n4n5t="                             "
  g=open(tape_in,"r")
  f=open(tape_out,"w")
  sec=""
  master=args.master
  
  for i,line in enumerate(g):
    line=line.rstrip("\n")
    line="{:<66s}".format(line)
    key="{:<10s}".format(line[0:10])
    alt="{:>1s}".format(line[79:80])+"\n"

    if i==0:
      if key=="LIB       " or\
         key=="REQUEST   " or\
         key=="BACKUP    " or\
         key=="MASTER    ":
        inp_typ="LIB"
      elif key=="TRANS     ":
        inp_typ="TRA"
      elif key=="ENTRY     ":
        inp_typ="ENT"
      elif key=="DICTION   ":
        inp_typ="DIC"
       
        time=datetime.datetime.now()
        date=time.strftime("%Y%m%d")

        cont="TRANS      "
        n1="       9"+"???"
        n2="   {:8s}".format(date)
        seq="9000000000000"
        f.write(cont+n1+n2+n3n4n5+seq+" \n")

    if (key=="LIB       " or\
          key=="REQUEST   " or\
          key=="BACKUP    " or\
          key=="MASTER    ") and\
          sec!="DIC":
      cont=line[0:11]
      n1=line[11:22]
      n2=line[22:33]
      seq="1000000000000"
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif (key=="ENDREQUEST" or\
          key=="ENDLIB    "   or\
          key=="ENDBACKUP "   or\
          key=="ENDMASTER ") and\
          sec!="DIC":
      cont=line[0:11]
      n1="{:>11d}".format(nan)
      n2="{:>11s}".format("0")
      seq=area+"999999999999"
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="TRANS     " and sec!="DIC":
      time=datetime.datetime.now()
      date=time.strftime("%Y%m%d")

      cont=line[0:11]
      tid=line[18:22]
      area=line[18:19]
      n1=line[11:22]

      if area=="9":
        n2="     {:6s}".format(date[0:6])
      else:
        n2="   {:8s}".format(date)

      seq=area+"000000000000"
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="ENDTRANS  " and sec!="DIC":
      cont=line[0:11]
      n1="{:>11d}".format(nan)
      n2="{:>11s}".format("0")
      seq=area+"999999999999"
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif (key=="ENTRY     " and sec!="DIC") or key=="DICTION   ":
      sec=""
      an=line[17:22]
      area=line[17:18]
      cont=line[0:11]
      n1=line[11:22]
      if line[24:26]=="  " and master==False:
        n2="   19"+line[27:33]
      else:
        n2=line[22:33]
      seq=an+"00000001"
      print("writing ... "+an)
      if inp_typ=="LIB":
        tidN5=line[62:66]
        f.write(cont+n1+n2+n3n4n5t+tidN5+seq+alt)
      else:
        f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif (key=="ENDENTRY  " and sec!="DIC") or key=="ENDDICTION":
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11d}".format(nsan[an])
      n2="{:>11s}".format("0")
      seq=an+"99999999"
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif (key=="SUBENT    " and sec!="DIC") or key=="SUBDICT   ":
      irec=1
      san=line[14:22]
      cont=line[0:11]
      n1=line[11:22]
      if line[24:26]=="  " and master==False:
        n2="   19"+line[27:33]
      else:
        n2=line[22:33]
      seq=san+"{:0>5d}".format(irec)

      if key=="SUBDICT   ":
        sec="DIC";
        desc=line[33:66]
        f.write(cont+n1+n2+desc+seq+alt)
      else:
        if inp_typ=="LIB":
          tidN5=line[62:66]
          f.write(cont+n1+n2+n3n4n5t+tidN5+seq+alt)
        else:
          f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif (key=="ENDSUBENT " and sec!="DIC") or key=="ENDSUBDICT":
      if key=="ENDSUBDICT":
        sec=""
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11d}".format(nrec[san])
      n2="{:>11s}".format("0")
      seq=san+"99999"
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="NOSUBENT  " and sec!="DIC":
      san=line[14:22]
      cont=line[0:11]
      n1=line[11:22]
      if re.compile("\S").search(line[27:33]):
        if line[24:26]=="  " and master==False:
          n2="   19"+line[27:33]
        else:
          n2=line[22:33]
      else:
        n2="           ";
      seq=san+"00001"
      if inp_typ=="LIB":
        tidN5=line[62:66]
        f.write(cont+n1+n2+n3n4n5t+tidN5+seq+alt)
      else:
        f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="BIB       " and sec!="DIC":
      irec+=1
      sec="BIB"
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
        n2=line[22:33]
      else:
        n1="{:>11d}".format(nkey[san])
        n2="{:>11d}".format(nbib[san])
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="ENDBIB    " and sec!="DIC":
      irec+=1
      sec=""
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11d}".format(nbib[san])
      n2="{:>11s}".format("0")
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="NOBIB     " and sec!="DIC":
      irec+=1
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11s}".format("0")
      n2="{:>11s}".format("0")
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="COMMON    " and sec!="DIC":
      irec+=1
      sec="COM"
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
        n2=line[22:33]
      else:
        n1="{:>11d}".format(mcom[san])
        n2="{:>11d}".format(ncom[san])
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="ENDCOMMON " and sec!="DIC":
      irec+=1
      sec=""
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11d}".format(ncom[san])
      n2="{:>11s}".format("0")
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="NOCOMMON  " and sec!="DIC":
      irec+=1
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11s}".format("0")
      n2="{:>11s}".format("0")
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="DATA      " and sec!="DIC" and sec!="DAT":
      irec+=1
      sec="DAT"
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
        n2=line[22:33]
      else:
        n1="{:>11d}".format(mdat[san])
        n2="{:>11d}".format(nlin[san])
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="ENDDATA   " and sec!="DIC":
      irec+=1
      sec=""
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11d}".format(ndat[san])
      n2="{:>11s}".format("0")
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    elif key=="NODATA    " and sec!="DIC":
      irec+=1
      cont=line[0:11]
      if master==True:
        n1=line[11:22]
      else:
        n1="{:>11s}".format("0")
      n2="{:>11s}".format("0")
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+n1+n2+n3n4n5+seq+alt)

    else:
      irec+=1
      cont=line[0:66]
      seq=san+"{:0>5d}".format(irec)
      f.write(cont+seq+alt)


  if inp_typ=="ENT":
    cont="ENDTRANS   "
    n1="{:>11d}".format(nan)
    n2="{:>11s}".format("0")
    seq=area+"999999999999"
    f.write(cont+n1+n2+n3n4n5+seq+alt)

def count(tape_in):
  nan=0
  sec=""
  f=open(tape_in,"r")

  sysid="          "
  for i,line in enumerate(f):
    line=line.rstrip("\n")
    key="{:<10s}".format(line[0:10])

    if i==0:
      if key=="LIB       " or\
         key=="REQUEST   " or\
         key=="BACKUP    " or\
         key=="MASTER    ":
        inp_typ="LIB"
      elif key=="TRANS     ":
        inp_typ="TRA"
      elif key=="ENTRY     ":
        inp_typ="ENT"
      elif key=="DICTION   ":
        inp_typ="DIC"
      else:
        msg="The first record must be TRANS or ENTRY."
        print_error_fatal(msg,line)

    if key=="LIB       " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="LIB       "

    elif key=="REQUEST   " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="REQUEST   "

    elif key=="BACKUP    " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="BACKUP    "

    elif key=="MASTER    " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="MASTER    "

    elif key=="TRANS     " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="TRANS     "

    elif key=="ENDLIB    " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDLIB    "

    elif key=="ENDREQUEST" and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDREQUEST"

    elif key=="ENDBACKUP " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDBACKUP "

    elif key=="ENDMASTER " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDMASTER "

    elif key=="ENDTRANS  " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDTRANS  "

    elif (key=="ENTRY     " and sec!="DIC") or key=="DICTION   ":
      if inp_typ!="ENT" and inp_typ!="DIC":
        check_sysid(key,sysid,line)
      if key=="DICTION   ":
        sysid="DICTION   "
      else:
        sysid="ENTRY     "
      sec=""
      an=line[17:22]
      nan+=1
      isan=0
      print("counting ... "+an)

    elif (key=="ENDENTRY  " and sec!="DIC") or key=="ENDDICTION":
      check_sysid(key,sysid,line)
      if key=="ENDDICTION":
        sysid="ENDDICTION"
      else:
        sysid="ENDENTRY  "
      nsan[an]=isan

    elif (key=="SUBENT    " and sec!="DIC") or key=="SUBDICT   ":
      check_sysid(key,sysid,line)
      if key=="SUBDICT   ":
        sysid="SUBDICT   "
        sec="DIC"
      else:
        sysid="SUBENT    "
      irec=0
      san=line[14:22]
      isan+=1

    elif key=="NOSUBENT  " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="NOSUBENT  "
      san=line[14:22]
      isan+=1

    elif (key=="ENDSUBENT " and sec!="DIC") or key=="ENDSUBDICT":
      check_sysid(key,sysid,line)
      if key=="ENDSUBDICT":
        sec=""
        sysid="ENDSUBDICT"
      else:
        sysid="ENDSUBENT "
      nrec[san]=irec
      if re.compile("001$").search(san): # common (001) subentry
        ndat[san]=0
        mdat[san]=0
        nlin[san]=0

    elif key=="BIB       " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="BIB       "
      irec+=1
      sec="BIB"
      ibib=0
      ikey=0

    elif key=="ENDBIB    " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDBIB    "
      irec+=1
      sec=""
      nbib[san]=ibib
      nkey[san]=ikey

    elif key=="NOBIB     " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="NOBIB     "
      irec+=1
      sec=""
      nbib[san]=0

    elif key=="COMMON    " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="COMMON    "
      irec+=1
      sec="COM"
      icom=0
      ifld=0

    elif key=="ENDCOMMON " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDCOMMON "
      irec+=1
      sec=""
      ncom[san]=icom
      mcom[san]=int(ifld/2)

    elif key=="NOCOMMON  " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="NOCOMMON  "
      irec+=1
      sec=""
      ncom[san]=0
      mcom[san]=0

    elif key=="DATA      " and sec!="DIC" and sec!="DAT":
      check_sysid(key,sysid,line)
      sysid="DATA      "
      irec+=1
      sec="DAT"
      idat=0
      ifld=0

    elif key=="ENDDATA   " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="ENDDATA   "
      irec+=1
      sec=""
      ndat[san]=idat
      mdat[san]=int(ifld/2)
      n=int((mdat[san]+5)/6)
      if ((ndat[san]-n*2)%n!=0):
        msg="The number of the data records incorrect."
        print_error_fatal(msg,line)
      else:
        nlin[san]=int((ndat[san]-n*2)/n)

    elif key=="NODATA    " and sec!="DIC":
      check_sysid(key,sysid,line)
      sysid="NODATA    "
      irec+=1
      sec=""
      ndat[san]=0
      mdat[san]=0

    elif sec!="BIB" and sec!="COM" and sec!="DAT" and sec!="DIC":
      msg="Unexpected system identifier found"
      print_error_fatal(msg,line)

    else: 
      irec+=1

      if sec=="BIB":
        ibib+=1 
        if re.compile("\S").search(key):
          ikey+=1

      elif sec=="COM" or sec=="DAT":
        if re.compile("\.").search(line): # data line with number
          pass

        elif re.compile("\S").search(line): # heading or unit
          for i in range(6):
            col1=11*i
            col2=col1+11
            char=line[col1:col2]
            if re.compile("\S").search(char):
              ifld+=1

        else: # data line without number
          pass
          
        if sec=="COM":
          icom+=1 
        elif sec=="DAT":
          idat+=1 

  return nan, nsan, nrec, nbib, nkey, ncom, mcom, ndat, mdat, nlin


def check_sysid(key,sysid,line):
  status=False
  if key=="LIB       " or  key=="REQUEST   "\
  or key=="BACKUP    " or  key=="MASTER    "\
  or key=="TRANS     ":
    if sysid=="          ":
      status=True
  elif key=="ENDLIB    " or key=="ENDREQUEST"\
    or key=="ENDBACKUP " or key=="ENDMASTER "\
    or key=="ENDTRANS  ":
    if sysid=="ENDENTRY  " or sysid=="ENDDICTION":
      status=True

  elif key=="ENTRY     " or key=="DICTION   ":
    if sysid=="LIB       " or sysid=="REQUEST   "\
    or sysid=="BACKUP    " or sysid=="MASTER    "\
    or sysid=="TRANS     "\
    or sysid=="ENDENTRY  " or sysid=="ENDDICTION":
      status=True

  elif key=="ENDENTRY  ":
    if sysid=="ENDSUBENT " or sysid=="NOSUBENT  ":
      status=True

  elif key=="ENDDICTION":
    if sysid=="ENDSUBDICT":
      status=True

  elif key=="SUBENT    " or key=="NOSUBENT  ":
    if sysid=="ENTRY     " or sysid=="ENDSUBENT "\
    or sysid=="NOSUBENT  ":
      status=True

  elif key=="SUBDICT   ":
    if sysid=="DICTION   " or sysid=="ENDSUBDICT":
      status=True

  elif key=="ENDSUBENT ":
    if sysid=="ENDDATA   " or sysid=="NODATA    "\
    or sysid=="ENDCOMMON " or sysid=="NOCOMMON  ":
      status=True

  elif key=="ENDSUBDICT":
    if sysid=="SUBDICT   ":
      status=True

  elif key=="BIB       " or key=="NOBIB     ":
    if sysid=="SUBENT    ":
      status=True

  elif key=="ENDBIB    ":
    if sysid=="BIB       ":
      status=True

  elif key=="COMMON    " or key=="NOCOMMON  ":
    if sysid=="ENDBIB    " or sysid=="NOBIB     ":
      status=True

  elif key=="ENDCOMMON ":
    if sysid=="COMMON    ":
      status=True

  elif key=="DATA      " or key=="NODATA    ":
    if sysid=="ENDCOMMON " or sysid=="NOCOMMON  ":
      status=True

  elif key=="ENDDATA   ":
    if sysid=="DATA      ":
      status=True

  if status==False:
    msg="Unexpected system identifier found after "+sysid+": "+key
    print_error_fatal(msg,line)

  return


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Add EXFOR record identification",\
          epilog="example: x4_seqadd.py -i trans.txt -o trans.ord")
  parser.add_argument("-v", "--version",\
         action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-m", "--master",\
   help="do not add 19 to two-digit year and do not alter N2 of END records", action="store_true")
  parser.add_argument("-i", "--tape_in",\
   help="name of input tape")
  parser.add_argument("-o", "--tape_out",\
   help="name of output tape")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_SEQADD (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  tape_in=args.tape_in
  if tape_in==None:
    tape_in=input("input file [exfor.txt] -------> ")
    if tape_in=="":
      tape_in="exfor.txt"
  if not os.path.exists(tape_in):
    print(" ** File "+tape_in+" does not exist.")
  while not os.path.exists(tape_in):
    tape_in=input("input file [exfor.txt] -------> ")
    if tape_in=="":
      tape_in="exfor.txt"
    if not os.path.exists(tape_in):
      print(" ** File "+tape_in+" does not exist.")

  tape_out=args.tape_out
  if tape_out==None:
    tape_out=input("output file [exfor_ord.txt] --> ")
  if tape_out=="":
    tape_out="exfor_ord.txt"
  if os.path.isfile(tape_out):
    msg="File '"+tape_out+"' exists and must be overwritten."
    print_error(msg,"")

  return tape_in,tape_out


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
