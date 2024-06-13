#!/usr/bin/python3
ver="2024-05-03"
######################################################
# X4_DICJ2A Ver. 2024-05-03
# (Converter from JSON Dictionary to Archive Dictionary)
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

  dictionary_list_add=["950"]
  dictionary_list=dictionary_list+dictionary_list_add

  time=datetime.datetime.now(timezone.utc)

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


# Produce Archive Dictionary
  print("printing archive dictionary   ... ", end="")
  for dict_id in dictionary_list:
    print(dict_id, end=" ")
    json_to_archive(dict_ver,dir_output,dict_id)
  print()

  print("Conversion completed. Good bye!")


def json_to_archive(dict_ver,dir_output,dict_id):
  time=datetime.datetime.now()
  file_out=dir_output+"/archive."+dict_id+"."+dict_ver

  if dict_id=="950":
    file_out=dir_output+"/dict_arc.top"
  else:
    file_out=dir_output+"/dict_arc_new."+dict_id
  f=open(file_out,'w')

  for key in dict_full[dict_id]:

    for item in dict_full[dict_id][key]:
      if dict_full[dict_id][key][item]==None:
        dict_full[dict_id][key][item]=""

    if key=="comment":
      for i,comment in enumerate(dict_full[dict_id][key]["comment"]):
        char=" "\
            +"%-3s"  % dict_full[dict_id][key]["status_code"]\
            +" "*39
        if dict_id=="005" or dict_id=="006" or\
           dict_id=="007" or dict_id=="015":
          char+=dict_full[dict_id][key]["comment"][i]["comment_flag"]
          char+=dict_full[dict_id][key]["comment"][i]["comment"]
        elif dict_id=="016":
          char+=dict_full[dict_id][key]["comment"][i]["comment"]
          char+=" "*(103-len(char))
          char+=dict_full[dict_id][key]["comment"][i]["comment_flag"]
        elif dict_id=="020" or dict_id=="037" or\
             dict_id=="236":
          char+=dict_full[dict_id][key]["comment"][i]
        elif dict_id=="033":
          char+="  "+dict_full[dict_id][key]["comment"][i]

        char+=" "*(123-len(char))
        f.write(char+"\n")

    else:

      if dict_id!="950":
        char="%-1s"  % dict_full[dict_id][key]["alteration_flag"]\
            +"%-3s"  % dict_full[dict_id][key]["status_code"]\
            +" "\
            +"%-6s"  % dict_full[dict_id][key]["date"]\
            +" "

      if dict_id=="001":
        char+=json_to_archive_001(key)
     
      elif dict_id=="002":
        char+=json_to_archive_002(key)
     
      elif dict_id=="003":
        char+=json_to_archive_003(key)
     
      elif dict_id=="004":
        char+=json_to_archive_004(key)
     
      elif dict_id=="005":
        char+=json_to_archive_005(key)
     
      elif dict_id=="006":
        char+=json_to_archive_006(key)
     
      elif dict_id=="007" or dict_id=="207":
        char+=json_to_archive_gen_1(key,dict_id)
     
      elif dict_id=="008":
        char+=json_to_archive_008(key)
     
      elif dict_id=="015":
        char+=json_to_archive_015(key)
     
      elif dict_id=="016":
        char+=json_to_archive_016(key)
     
      elif dict_id=="017":
        char+=json_to_archive_017(key)
     
      elif dict_id=="018" or dict_id=="021" or\
           dict_id=="022" or dict_id=="023":
        char+=json_to_archive_gen_2(key,dict_id)
     
      elif dict_id=="019":
        char+=json_to_archive_019(key)
     
      elif dict_id=="020" or dict_id=="037" or\
           dict_id=="038":
        char+=json_to_archive_gen_3(key,dict_id)
     
      elif dict_id=="024":
        char+=json_to_archive_024(key)
     
      elif dict_id=="025":
        char+=json_to_archive_025(key)
     
      elif dict_id=="026":
        char+=json_to_archive_026(key)
     
      elif dict_id=="030":
        char+=json_to_archive_030(key)
     
      elif dict_id=="031":
        char+=json_to_archive_031(key)
     
      elif dict_id=="032":
        char+=json_to_archive_032(key)
     
      elif dict_id=="033":
        char+=json_to_archive_033(key)
     
      elif dict_id=="034":
        char+=json_to_archive_034(key)
     
      elif dict_id=="035":
        char+=json_to_archive_035(key)
     
      elif dict_id=="043":
        char+=json_to_archive_043(key)
     
      elif dict_id=="045":
        char+=json_to_archive_045(key)
     
      elif dict_id=="047":
        char+=json_to_archive_047(key)
     
      elif dict_id=="048":
        char+=json_to_archive_048(key)
     
      elif dict_id=="052":
        char+=json_to_archive_052(key)
     
      elif dict_id=="113":
        char+=json_to_archive_113(key)
     
      elif dict_id=="144":
        char+=json_to_archive_144(key)
     
      elif dict_id=="209":
        char+=json_to_archive_209(key)
     
      elif dict_id=="213":
        char+=json_to_archive_213(key)
     
      elif dict_id=="227":
        char+=json_to_archive_227(key)
     
      elif dict_id=="235":
        char+=json_to_archive_235(key)
     
      elif dict_id=="236":
        char+=json_to_archive_236(key)
     
      elif dict_id=="950":
        char=json_to_archive_top(key)

      f.write(char+"\n")

      if "long_expansion" in dict_full[dict_id][key]:
        long_expansion=dict_full[dict_id][key]["long_expansion"]
        if long_expansion!="":
          print_long_expansion_archive(f,long_expansion,key,dict_id)

      if "comment" in dict_full[dict_id][key]:
        for i, comment in enumerate(dict_full[dict_id][key]["comment"]):
          if dict_id=="003" or dict_id=="005" or\
             dict_id=="006" or dict_id=="007" or\
             dict_id=="016" or dict_id=="034" or\
             dict_id=="207":
            comment_flag=dict_full[dict_id][key]["comment"][i]["comment_flag"]
            comment=dict_full[dict_id][key]["comment"][i]["comment"]
            char="%-1s"  % dict_full[dict_id][key]["alteration_flag"]\
                +"%-3s"  % dict_full[dict_id][key]["status_code"]\
                +" "*8\
                +" "*31

            if dict_id=="016":
              char=char\
                  +comment
            else:
              char=char\
                  +comment_flag\
                  +comment
           
          elif dict_id=="033" or dict_id=="209":
            char="%-1s"  % dict_full[dict_id][key]["alteration_flag"]\
                +"%-3s"  % dict_full[dict_id][key]["status_code"]\
                +" "*8\
                +" "*31\
                +" "*2\
                +comment

          else:
            char="%-1s"  % dict_full[dict_id][key]["alteration_flag"]\
                +"%-3s"  % dict_full[dict_id][key]["status_code"]\
                +" "*8\
                +" "*31\
                +comment\
       
       
          char+=" "*(123-len(char))
          f.write(char+"\n")

  f.close()


def json_to_archive_001(key):
  char="%-10s" % key\
      +" "*21\
      +"%9s"   % dict_full["001"][key]["internal_numerical_equivalent"]\
      +" "\
      +"%-55s" % dict_full["001"][key]["expansion"]\
      +" "*15

  return char


def json_to_archive_002(key):
  char="%-10s" % key\
      +" "*21\
      +"%-25s" % dict_full["002"][key]["expansion"]\
      +"%-1s"  % dict_full["002"][key]["keyword_required"]\
      +"%2s"   % dict_full["002"][key]["internal_numerical_equivalent"]\
      +"%-1s"  % dict_full["002"][key]["code_required"]\
      +"%3s"   % dict_full["002"][key]["pointer_to_related_dictionary"]\
      +" "*48

  return char


def json_to_archive_003(key):
  char="%-7s"  % key\
      +" "*24\
      +"%-3s"  % dict_full["003"][key]["cinda_code"]\
      +"%-1s"  % dict_full["003"][key]["area_code"]\
      +"%-3s"  % dict_full["003"][key]["country_code"]\
      +"%-53s" % dict_full["003"][key]["expansion"]\
      +"%-15s" % dict_full["003"][key]["country_for_cinda"]\
      +" "*5

  return char


def json_to_archive_004(key):
  char="%-1s"  % key\
      +" "*30\
      +"%-4s"  % dict_full["004"][key]["short_expansion"]\
      +"%3s"   % dict_full["004"][key]["pointer_to_related_dictionary"]\
      +"%-35s" % dict_full["004"][key]["expansion"]\
      +" "*38

  return char


def json_to_archive_005(key):
  char="%-6s"  % key\
      +" "*25\
      +"%-4s"  % dict_full["005"][key]["cinda_code"]\
      +"%-1s"  % dict_full["005"][key]["area_code"]\
      +"%-3s"  % dict_full["005"][key]["country_code"]\
      +"%-1s"  % dict_full["005"][key]["additional_area_code"]\
      +"%-3s"  % dict_full["005"][key]["additional_country_code"]\
      +"%-20s" % dict_full["005"][key]["short_expansion"]\
      +"%-48s" % dict_full["005"][key]["expansion"]\

  return char


def json_to_archive_006(key):
  char="%-11s" % key\
      +" "*20\
      +"%-7s"  % dict_full["006"][key]["institute_code"]\
      +"%-48s" % dict_full["006"][key]["expansion"]\
      +"%-1s"  % dict_full["006"][key]["cinda_flag"]\
      +" "*24

  return char


def json_to_archive_gen_1(key,dict_id):
  char="%-10s" % key\
      +" "*21\
      +"%-53s" % dict_full[dict_id][key]["expansion"]\
      +"%-1s"  % dict_full[dict_id][key]["area_code"]\
      +"%-3s"  % dict_full[dict_id][key]["country_code"]\
      +"%-1s"  % dict_full[dict_id][key]["additional_area_code"]\
      +"%-3s"  % dict_full[dict_id][key]["additional_country_code"]\
      +"%-10s" % dict_full[dict_id][key]["cinda_short_code"]\
      +" "*9

  return char


def json_to_archive_008(key):
  char="%3s"   % key\
      +" "*28\
      +"%-2s"  % dict_full["008"][key]["element_symbol"]\
      +"%-20s" % dict_full["008"][key]["element_name"]\
      +" "*58

  return char


def json_to_archive_015(key):
  char="%-1s"  % key\
      +" "*30\
      +"%-15s" % dict_full["015"][key]["short_expansion"]\
      +"%-37s" % dict_full["015"][key]["expansion"]\
      +" "*28

  return char


def json_to_archive_016(key):
  char="%-5s"  % key\
      +" "*26\
      +"%5s"   % dict_full["016"][key]["internal_numerical_equivalent"]\
      +"%-52s" % dict_full["016"][key]["expansion"]\
      +" "*3\
      +"%-1s"  % dict_full["016"][key]["subentry_number_field_flag"]\
      +" "*19

  return char


def json_to_archive_017(key):
  char="%-1s"  % key\
      +" "*30\
      +"%-53s" % dict_full["017"][key]["expansion"]\
      +" "*27

  return char


def json_to_archive_gen_2(key,dict_id):
  char="%-5s"  % key\
      +" "*26\
      +"%-53s" % dict_full[dict_id][key]["expansion"]\
      +"%-4s"  % dict_full[dict_id][key]["special_use_flag"]\
      +" "*23

  return char


def json_to_archive_019(key):
  char="%-5s"  % key\
      +" "*26\
      +"%-53s" % dict_full["019"][key]["expansion"]\
      +"%-4s"  % dict_full["019"][key]["special_use_flag"]\
      +"%-1s"  % dict_full["019"][key]["delimiter_flag"]\
      +" "*22

  return char


def json_to_archive_gen_3(key,dict_id):
  char="%-5s"  % key\
      +" "*26\
      +"%-53s" % dict_full[dict_id][key]["expansion"]\
      +" "*27

  return char


def json_to_archive_024(key):
  char="%-10s" % key\
      +" "*21\
      +"%-1s"  % dict_full["024"][key]["data_type_flag_1"]\
      +"%-1s"  % dict_full["024"][key]["data_type_flag_2"]\
      +"%-1s"  % dict_full["024"][key]["family_flag"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_1"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_2"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_3"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_4"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_5"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_6"]\
      +"%-1s"  % dict_full["024"][key]["plotting_flag_7"]\
      +"%-4s"  % dict_full["024"][key]["unit_family_code"]\
      +" "\
      +"%-54s" % dict_full["024"][key]["expansion"]\
      +" "*6\
      +"%-4s"  % dict_full["024"][key]["special_use_flag"]\
      +" "

  return char


def json_to_archive_025(key):
  char="%-10s"  % key\
      +" "*21\
      +"%-33s"  % dict_full["025"][key]["expansion"]\
      +" "*2\
      +"%-4s"   % dict_full["025"][key]["unit_family_code"]\

  conversion_factor=dict_full["025"][key]["conversion_factor"]
  if conversion_factor=="":
    char+="           "
  else:
    char+="%11.4E" % conversion_factor

  char+="%-3s"   % dict_full["025"][key]["sorting_flag"]\
      +" "*27

  return char


def json_to_archive_026(key):
  char="%-4s" % key\
      +" "*27\
      +"%-2s"  % dict_full["026"][key]["dictionary_24_use"]\
      +"%-2s"  % dict_full["026"][key]["dictionary_25_use"]\
      +"%-2s"  % dict_full["026"][key]["dictionary_236_use"]\
      +"%-50s" % dict_full["026"][key]["expansion"]\
      +" "*24

  return char


def json_to_archive_030(key):
  char="%-3s" % key\
      +" "*28\
      +"%10s"  % dict_full["030"][key]["internal_numerical_equivalent"]\
      +"%-55s" % dict_full["030"][key]["expansion"]\
      +"%-4s"  % dict_full["030"][key]["special_use_flag"]\
      +" "*11

  return char


def json_to_archive_031(key):
  char="%-5s" % key\
      +" "*26\
      +"%10s"  % dict_full["031"][key]["internal_numerical_equivalent"]\
      +"%-55s" % dict_full["031"][key]["expansion"]\
      +"%-4s"  % dict_full["031"][key]["special_use_flag"]\
      +" "*11

  return char


def json_to_archive_032(key):
  char="%-3s" % key\
      +" "*28\
      +"%10s"  % dict_full["032"][key]["internal_numerical_equivalent"]\
      +"%-55s" % dict_full["032"][key]["expansion"]\
      +"%-4s"  % dict_full["032"][key]["special_use_flag"]\
      +" "*11

  return char


def json_to_archive_033(key):
  char="%-6s" % key\
      +" "*25\
      +"%6s"   % dict_full["033"][key]["internal_numerical_equivalent_1"]\
      +"%5s"   % dict_full["033"][key]["internal_numerical_equivalent_2"]\
      +"%-1s"  % dict_full["033"][key]["allowed_subfield_flag_1"]\
      +"%-1s"  % dict_full["033"][key]["allowed_subfield_flag_2"]\
      +"%-1s"  % dict_full["033"][key]["allowed_subfield_flag_3"]\
      +"%-1s"  % dict_full["033"][key]["allowed_subfield_flag_4"]\
      +"%-40s" % dict_full["033"][key]["expansion"]\
      +" "*25

  return  char


def json_to_archive_034(key):
  char="%-5s" % key\
      +" "*26\
      +"%10s"  % dict_full["034"][key]["internal_numerical_equivalent"]\
      +"%-5s"  % dict_full["034"][key]["general_quantity_modifier_flag"]\
      +"%-55s" % dict_full["034"][key]["expansion"]\
      +"%-4s"  % dict_full["034"][key]["special_use_flag"]\
      +" "*6

  return  char


def json_to_archive_035(key):
  char="%-5s" % key\
      +" "*26\
      +"%10s"  % dict_full["035"][key]["internal_numerical_equivalent"]\
      +"%-40s" % dict_full["035"][key]["expansion"]\
      +" "*30

  return  char


def json_to_archive_043(key):
  char="%2s"   % key\
      +" "*29\
      +"%-55s" % dict_full["043"][key]["expansion"]\
      +" "*25

  return char


def json_to_archive_045(key):
  char="%-3s"  % key\
      +" "*28\
      +"%-3s"  % dict_full["045"][key]["web_quantity_code"]\
      +" "*4\
      +"%-48s" % dict_full["045"][key]["expansion"]\
      +" "*25

  return char


def json_to_archive_047(key):
  char="%-3s"  % key\
      +" "*28\
      +"%-10s" % dict_full["047"][key]["cinda_reaction_code"]\
      +"%-3s"  % dict_full["047"][key]["cinda_quantity_code"]\
      +" "*2\
      +"%-1s"  % dict_full["047"][key]["flag"]\
      +" "*64

  return char


def json_to_archive_048(key):
  char="%-5s"  % key\
      +" "*26\
      +"%-10s" % dict_full["048"][key]["short_expansion"]\
      +"%-45s" % dict_full["048"][key]["expansion"]\
      +" "*25

  return char


def json_to_archive_052(key):
  char="%-2s"  % key\
      +" "*29\
      +"%-55s" % dict_full["052"][key]["expansion"]\
      +" "*5\
      +"%-15s" % dict_full["052"][key]["country"]\
      +" "*5

  return char


def json_to_archive_113(key):
  char="%-3s"  % key\
      +" "*28\
      +"%-55s" % dict_full["113"][key]["expansion"]\
      +" "*25

  return char


def json_to_archive_144(key):
  char="%-13s" % key\
      +" "*18\
      +"%-1s"  % dict_full["144"][key]["area_code"]\
      +"%-3s"  % dict_full["144"][key]["country_code"]\
      +"%-1s"  % dict_full["144"][key]["additional_area_code"]\
      +"%-3s"  % dict_full["144"][key]["additional_country_code"]\
      +"%-52s" % dict_full["144"][key]["expansion"]\
      +" "*20

  return char


def json_to_archive_209(key):
  key_out=key.strip()
  arrays=key.split("-")
  if float(arrays[0])<10:
    key_out="  "+key_out
  elif float(arrays[0])<100:
    key_out=" "+key_out

  char="%-10s" % key_out\
      +" "*21\
      +"%-5s"  % dict_full["209"][key]["cinda_code"]\
      +"%6s"   % dict_full["209"][key]["internal_numerical_equivalent"]\
      +" "*29\
      +"%-25s" % dict_full["209"][key]["expansion"]\
      +" "*5\
      +"%-1s"  % dict_full["209"][key]["compound_flag"]\
      +" "*9

  return char


def json_to_archive_213(key):
  char="%-4s" % key\
      +" "*27\
      +"%-3s"  % dict_full["213"][key]["cinda_quantity_code"]\
      +" "*2\
      +"%-3s"  % dict_full["213"][key]["web_quantity_code"]\
      +" "\
      +"%2s"   % dict_full["213"][key]["sorting_flag"]\
      +" "\
      +"%-1s"  % dict_full["213"][key]["independent_variable_family_flag_1"]\
      +" "\
      +"%-1s"  % dict_full["213"][key]["independent_variable_family_flag_3"]\
      +"%-1s"  % dict_full["213"][key]["independent_variable_family_flag_4"]\
      +"%-1s"  % dict_full["213"][key]["independent_variable_family_flag_5"]\
      +"%-1s"  % dict_full["213"][key]["independent_variable_family_flag_6"]\
      +"%-1s"  % dict_full["213"][key]["independent_variable_family_flag_7"]\
      +" "\
      +" "\
      +" "\
      +"%-46s" % dict_full["213"][key]["expansion"]\
      +" "*12

  return char


def json_to_archive_227(key):

  key_out=key.strip()
  arrays=key.split("-")
  if float(arrays[0])<10:
    key_out="  "+key_out
  elif float(arrays[0])<100:
    key_out=" "+key_out

  char="%-13s" % key_out\
      +" "*24\
      +"%7s"    % dict_full["227"][key]["internal_numerical_equivalent"]\
      +"%-1s"   % dict_full["227"][key]["use_flag"]\
      +"%-6s"   % dict_full["227"][key]["spin_and_parity"]\
      +"%-1s"   % dict_full["227"][key]["state_ordering_flag"]\

  half_life=dict_full["227"][key]["half-life"]
  if half_life=="":
    char+="           "
  else:
    char+="%11.4E" % half_life

  char+="%-1s"   % dict_full["227"][key]["decay_flag"]\
       +" "*2\

  isotopic_abundance=dict_full["227"][key]["isotopic_abundance"]
  if isotopic_abundance=="":
    char+="           "
  else:
    char+="%11.4E" % isotopic_abundance

  atomic_weight=dict_full["227"][key]["atomic_weight"]
  if atomic_weight=="":
    char+="            "
  else:
    char+="%12.5E" % atomic_weight

  char+="%-21s"  % dict_full["227"][key]["explanation"]\
       +" "

  return char


def json_to_archive_235(key):
  char="%-1s"  % key\
      +" "*30\
      +"%-4s"  % dict_full["235"][key]["short_expansion"]\
      +" "*2\
      +"%-35s" % dict_full["235"][key]["expansion"]\
      +" "*39

  return char


def json_to_archive_236(key):
  char="%-30s" % key\
      +" "\
      +"%-3s"  % dict_full["236"][key]["reaction_type_code"]\
      +" "\
      +"%-4s"  % dict_full["236"][key]["unit_family_code"]\
      +"%-1s"  % dict_full["236"][key]["resonance_flag"]\
      +"%-71s" % dict_full["236"][key]["expansion"]\

  return char


def json_to_archive_top(key):
  key_out=key
  key_out=re.sub("^00", '  ', key_out);
  key_out=re.sub("^0", ' ', key_out);
  char="%-3s"  % key_out\
      +" "\
      +"%-30s" % dict_full["950"][key]["dictionary_name"]\
      +" "\
      +"%2s"   % dict_full["950"][key]["number_of_daniel_keys"]\
      +" "\
      +"%-44s" % dict_full["950"][key]["formats_of_key_and_expansion_fields"]\
      +" "*41

  return char


def print_long_expansion_archive(f,long_expansion,key,dict_id):
  long_expansion="("+long_expansion+")"
  chars=list(long_expansion)

  char0="%-1s"  % dict_full[dict_id][key]["alteration_flag"]\
       +"%-3s"  % dict_full[dict_id][key]["status_code"]\
       +" "*8\
       +" "*30\

  text=char0+" "
  text1=char0+" "

  if dict_id=="236":
    len_max=87
  else:
    len_max=98

  for i,char in enumerate(chars):
    text+=char
    text1+=char
    if len(text)>len_max:
      text0="%-123s" % text0
      f.write(text0+"\n")
      text=text1
    elif i==len(chars)-1:
      text="%-123s" % text
      f.write(text+"\n")
    elif chars[i+1]==" ":
      text0=text
      text1=char0+" "
#   elif chars[i+1]==".":
#     text0=text
#     text1=char0+" "

  return


def get_args(ver):
  global args

  parser=argparse.ArgumentParser(\
          usage="Convert JSON Dictionary to Archive Dictionaries",\
          epilog="example: x4_dicj2a.py -n 9128 -i input -o output")
  parser.add_argument("-v", "--version",\
         action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-n", "--dict_ver",\
   help="dictionary version (transmission ID)")
  parser.add_argument("-i", "--dir_input",\
   help="name of input JSON Dictionary directory")
  parser.add_argument("-o", "--dir_output",\
   help="name of output Archive Dictionary directory")

  args=parser.parse_args()


def get_input():
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4_DICJ2A (Ver-"+ver+") run on "+date)
  print("--------------------------------------------")

  dict_ver=args.dict_ver
  if dict_ver==None:
    dict_ver=input("input dictionary version [9128] --------------> ")
    if dict_ver=="":
      dict_ver="9128"
  if not re.compile("^9\d{3,3}$").search(dict_ver):
    print(" ** Dictionary version must be a 4-digit integer starting from 9.")
  while not re.compile("^\d{4,4}$").search(dict_ver):
    dict_ver=input("input dictionary version [9128] --------------> ")
    if dict_ver=="":
      dict_ver="9128"
    if not re.compile("^9\d{3,3}$").search(dict_ver):
      print(" ** Dictionary version must be a 4-digit integer starting from 9.")

  dir_input=args.dir_input
  if dir_input==None:
    dir_input=input("input JSON Dictionary directory [input] ------> ")
    if dir_input=="":
      dir_input="input"
    file_in=dir_input+"/dict."+dict_ver+".json"
    if not os.path.isfile(file_in):
      print(" ** JSON Dictionary "+file_in+" does not exist.")
  while not os.path.isfile(file_in):
    dir_input=input("input JSON Dictionary directory [input] ------> ")
    if dir_input=="":
      dir_input="input"
    file_in=dir_input+"/dict."+dict_ver+".json"
    if not os.path.isfile(file_in):
      print(" ** JSON Dictionary "+file_in+" does not exist.")

  dir_output=args.dir_output
  if dir_output==None:
    dir_output=input("output Archive Dictionary directory [output] -> ")
  if dir_output=="":
    dir_output="output"

  if os.path.isdir(dir_output):
    msg="Directory '"+dir_output+"' exists and must be overwritten."
    print_error(msg,"")
  else:
    msg="Directionry '"+dir_output+"' does not exist and must be created."
    print_error(msg,"")
    os.mkdir(dir_output)

  return dict_ver, dir_input, dir_output


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
