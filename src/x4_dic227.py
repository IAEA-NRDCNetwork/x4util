#!/usr/bin/python3
ver="2024-05-03"
######################################################
# X4_DIC227 Ver. 2024-05-03
# (Converter from Nubase to Archive Dict. 227)
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
  amu=931494.10242 # 1 keV/u

  get_args(ver)
  (file_inpnu,file_inpsp,file_out,ruler)=get_input()

  lines=get_file_lines(file_inpnu)

  time=datetime.datetime.now()
  date_out=time.strftime("%Y%m")

  line_dic=dict()
  for line in lines:

    if re.compile("^#").search(line):
      continue

    mass=line[0:3] # mass number
    mass=re.sub("^0+","",mass)

    elem=line[4:7] # atomic number
    if elem=="000": # neutron
      elem="0"
    else:
      elem=re.sub("^0+","",elem)

    char=int(line[7:8]) # isomeric state (0: G, i: Mi)
    if char==0:
      isom=0

    symb=line[11:16] # symbol
    if re.compile("1n").search(symb):
      symb="NN"
    else:
      regex=re.compile("^{}".format(mass))
      symb=regex.sub("",symb)
      symb=re.sub("\s+$","",symb)
      symb=symb.upper()

    isou=line[67:68] # isomeric uncertain

    if isou=="*" and isom==0: # g.s. but g.s. and m.s. ordering uncertain)
      code=elem+"-"+symb+"-"+mass
    elif float(isom)>0:       # a metastable state
      code=elem+"-"+symb+"-"+mass+"-M"
    else:
      code=elem+"-"+symb+"-"+mass
    code="%-12s" % code

    if symb=="NN":
      asmb="N     "
    else:
      asmb=symb+mass
      asmb=re.sub("\s","",asmb)
      asmb="%-6s" % asmb

    spin_parity=line[88:102] # spin/parity
    if "*" in spin_parity and  "(" not in spin_parity: # strong experimental argument
      spin_parity=re.sub("T=.+","",spin_parity)  # exclude isospin multiplet value T=...
      spin_parity=re.sub("\*\s+","",spin_parity) # excluding the directly meausred flag *
      spin=spin_parity[0:-1]
      parity=spin_parity[-1]

      if "/" in spin:
        arrays=spin.split("/") 
        spin=float(arrays[0])/float(arrays[1])
      else:
        spin=spin+".0"

      spin="%-5s" % spin
    else:
      parity=" "
      spin="     "

    hlf=line[69:78] # half-life value
    un1=line[78:79] # half-life unit (1st char)
    if un1=="m":
      fac=1.E-03
    elif un1=="u":
      fac=1.E-06
    elif un1=="n":
      fac=1.E-09
    elif un1=="p":
      fac=1.E-12
    elif un1=="f":
      fac=1.E-15
    elif un1=="a":
      fac=1.E-18
    elif un1=="z":
      fac=1.E-21
    elif un1=="y":
      fac=1.E-24
    elif un1=="k":
      fac=1.E+03
    elif un1=="M":
      fac=1.E+06
    elif un1=="G":
      fac=1.E+09
    elif un1=="T":
      fac=1.E+12
    elif un1=="P":
      fac=1.E+15
    elif un1=="E":
      fac=1.E+18
    elif un1=="Z":
      fac=1.E+21
    elif un1=="Y":
      fac=1.E+24
    elif un1==" ":
      fac=1

    un2=line[79:80] # half-life unit (2nd char)
    if un2=="s":
      fac=fac*1
    elif un2=="m":
      fac=fac*60
    elif un2=="h":
      fac=fac*3600
    elif un2=="d":
      fac=fac*86400
    elif un2=="y":
      fac=fac*31556926

    if hlf==" stbl    ": # T1/2=0 for stable nuclide (This must be first selection. e.g., 180Ta)
      hlfv=0
      hlf="           "
      hlfun="S  "
    elif not re.compile("\S").search(hlf): # T1/2 not given
      hlfv=0
      hlf="           "
      hlfun="U  "
    elif hlf==" p-unst  ": # T1/2=blank for particle unstable state
      hlfv=0
      hlf="           "
      hlfun="P  "
    elif "<" in hlf:       # T1/2 upper boundary given
      hlfv=0
      hlf="           "
      hlfun="U  "
    elif "#" in hlf:       # T1/2 from systematics
      hlfv=0
      hlf="           "
      hlfun="U  "
    elif ">" in hlf:       # T1/2 lower boundary given
      hlfv=re.sub("(>|~|\s)","",hlf)
      hlfv=float(hlfv)*fac
      hlf="           "
      hlfun="U  "
    else:                  # T1/2 for addition in Dict.
      hlf=re.sub("~","",hlf)
      hlf=float(hlf)*fac
      hlf="%11.4E" % hlf
      hlfv=hlf
      hlfun="U  "

    if isom!=0:  # not a g.s.
#     if hlfun=="   ":     # stable isomer (180Ta)
      if hlfun=="S  ":     # stable isomer (180Ta)
        pass
      elif not re.compile("\d").search(hlf): # T1/2 not given
        if hlfv>=1: # state having lower boundary or systematic value is kept
          msg="Warning: Lower boundary or systematics value is given for T1/2"
          print_error(msg,line)
        else:
          continue
      elif float(hlf)<0.1:          # T1/2<0.1 sec
        continue

    arrays=line[119:209].split(";") # isotopic abundance (IT probablity ignored)
    abun=""
    for item in arrays:
      item=re.sub("\s\d+","",item) # remove uncertaity
      if re.compile("^IS=((\d|\+|-|\.)+)$").search(item):
        abun=re.search("(\d|\+|-|\.)+",item).group()
        if not re.compile("^\d+(\.\d+)?$").search(abun):
          msg="Error: Isotopic abundance is not a fixed decimal pointer number!"
          print_error_fatal(msg,line)
#       elif not re.compile("\.").search(abun):
#         abun=abun+"."
#       abun="%-11s"  % abun
        abun="%11.4E" % float(abun)
   
      if not re.compile("\d").search(abun):
        abun="           "
  
    nume=10000*int(elem)+10*int(mass)+isom # Internal numerical equivalent
    nume="%7s" % nume
    isom+=1
   
    amas=line[18:31] # Mass excess
    if "#" in amas: # excluding mass excess from systematics 
      amas="            "
    elif re.compile("\d").search(amas):
      amas=float(re.sub("\s","",amas))
      amas=(amas+float(mass)*amu)/amu # Mass excess -> Atomic mass (in amu)
#     amas="%9.5f"  % amas
#     amas=amas+"  "
      amas="%12.5E" % amas
    else:
      amas="          "
   
    char="MTRA "+date_out+" "
    char+=code
    char+="                   "
    char+=asmb
    char+=nume
    char+=" "    # Use flag
    char+=parity
    char+=spin
#   char+=" "    # half-life flag (currently not in use)
    char+=isou
    char+=hlf
    char+=hlfun  # half-life unit (U: unstable, P: particle unstable)
    char+=abun
    char+=amas
    if nume in line_dic:
      msg="Error: Internal numerical equivalent is defined twice!"
      print_error_fatal(msg,line)
    else:
      line_dic[nume]=char

  numes=line_dic.keys()
  numes=sorted(numes)

  array=[]
  niso=dict()
  for nume in numes:
    asmb=line_dic[nume][43:49]
    if asmb in niso and re.compile("\w").search(asmb):
      niso[asmb]+=1 # g.s./m.s. counter for each (Z,A)
    else:
      niso[asmb]=0
    array.append(line_dic[nume])

# addition of -G and replacement of -M with -M1 etc.
  line_out=dict()
  iout=dict()
  for item in array:
    code=item[12:25]
    code_org=code

#   if not re.compile("-A\s*$").search(code): # isomeric flagging -G, -M1 and -M2
    asmb=item[43:49]
    if niso[asmb]>0 and not re.compile("-M\s*$").search(code): # g.s. for which a m.s. exists
      code=re.sub("\s+$","",code)
      code=code+"-G"
    elif niso[asmb]>1 and re.compile("-M\s*$").search(code):   # m.s. for which several m.s. exist
      if asmb in iout:    # 2nd, 3rd, ... m.s.
        iout[asmb]+=1
      else:               # 1st m.s.
        iout[asmb]=1
   
      code=re.sub("\s+$","",code)
      code+=str(iout[asmb])


#   code=re.sub(\s+$,"",code)
    code="%-13s" % code

# To set the last digit of the Z number at col.15
    elem=re.search("^\d+",code).group()
    if float(elem)<10:
      code=re.sub("  $","",code)
      code="  "+code
    elif float(elem)<100:
      code=re.sub(" $","",code)
      code=" "+code
    
    nume=item[49:56]
    line_out[nume]=re.sub(code_org,code,item) # addition of flag


# Addition of particles and natural isotopic mixtures
  lines=get_file_lines(file_inpsp)

  for line in lines:
    if re.compile("\d").search(line[89:101]):
      amas="%12.5E" % float(line[89:101])
    else:
      amas="            "
    char=line[0:43]+"      "+line[49:89]+amas+line[101:123] # removal of the symbol
    nume=line[49:56]

    if nume in line_out:
      msg="Error: Internal numerical equivalent is defined twice!"
      print_error_fatal(msg,line)
    else:
      line_out[nume]=char


# Final output
  f=open(file_out,'w')
  
  if ruler=="Y":
    f.write("----+----1----+----2----+----3----+----4----+----5----+----6")
    f.write("----+----7----+----8----+----9----+----0----+----1----+----2---\n")

  numes=line_out.keys()
  numes=[int(i) for i in numes]
  numes=sorted(numes)
  numes=[str(i) for i in numes]
  numes=["{0:>7}".format(i) for i in numes]

  for nume in numes:
    char=line_out[nume][0:43]+"      "+line_out[nume][49:123] # output of A-symbol suspended
    char="%-123s" % char
    f.write(char+"\n")

  f.close()

  print("Conversion Completed. Good bye!")


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Convert NUBASE to Archive Dictionary 227",\
          epilog="example: x4_dic227.py -n nubase_3.mas20.txt -s dict_227-sup.txt -o dict_arc_new.227")
  parser.add_argument("-v", "--version",\
         action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-i", "--file_inpnu",\
   help="name of input NUBASE file")
  parser.add_argument("-s", "--file_inpsp",\
   help="name of supplemental (particle) input file")
  parser.add_argument("-o", "--file_out",\
   help="name of output Archive file")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_DIC227 (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  file_inpnu=args.file_inpnu
  if file_inpnu==None:
    file_inpnu=input("input Nubase file name [nubase_3.mas20.txt] -----> ")
    if file_inpnu=="":
      file_inpnu="nubase_3.mas20.txt"
  if not os.path.isfile(file_inpnu):
    print(" ** File "+file_inpnu+" does not exist.")
  while not os.path.isfile(file_inpnu):
    file_inpnu=input("input Nubase file name [nubase_3.mas20.txt] -----> ")
    if file_inpnu=="":
      file_inpnu="nubase_3.mas20.txt"
    if not os.path.isfile(file_inpnu):
      print(" ** File "+file_inpnu+" does not exist.")

  file_inpsp=args.file_inpsp
  if file_inpsp==None:
    file_inpsp=input("input supplemental file name [dict_227-sup.txt] -> ")
    if file_inpsp=="":
      file_inpsp="dict_227-sup.txt"
  if not os.path.isfile(file_inpsp):
    print(" ** File "+file_inpsp+" does not exist.")
  while not os.path.isfile(file_inpsp):
    file_inpsp=input("input supplemental file name [dict_227-sup.txt] -> ")
    if file_inpsp=="":
      file_inpsp="dict_227-sup.txt"
    if not os.path.isfile(file_inpsp):
      print(" ** File "+file_inpsp+" does not exist.")

  file_out=args.file_out
  if file_out==None:
    file_out=input("output Archive file name [dict_arc_new.227] -----> ")
  if file_out=="":
    file_out="dict_arc_new.227"
  if os.path.isfile(file_out):
    msg="File '"+file_out+"' exists and must be overwritten."
    print_error(msg,"")

  ruler="N"
# while ruler!="Y" and ruler!="N":
#   ruler=input("print ruler Y/N? [Y] ----------------------------> ")
#   if ruler=="":
#     ruler="Y"
#   if ruler!="Y" and ruler!="N":
#     print(" ** Anser must be Y or N.")

  return file_inpnu,file_inpsp,file_out,ruler


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
  main()
  exit()
