import random
import configparser
import os
from termcolor import cprint

os.chdir(os.path.abspath(os.path.dirname(__file__))) #to avoid incoming issue regarding working dir
setin=configparser.ConfigParser()
_DEFAULT_VALUES = {
  "enable_timer": True,
  "record_display": 0,
  "isLocal": True,
  "maxnum": 99,
  "decimal_digits": 2
}
WARN_IGNORE=False #set to TRUE to disable the warning when you set an invalid value on the settings

try:
  setin.read("meg_stg.ini") #the name of the file for saved settings is here!
  def get_settings(option):
    try:
      if (option.lower() in ("enable_timer", "islocal")):
        a=setin["DEFAULT"][option].upper()
        if not (a in ("FALSE", "TRUE")):
          if not WARN_IGNORE:
            cprint(f"[ERROR - saved settings] Invalid value: on the <{option}> option, please set a valid value as explained in the comments.", "light_red")
          return _DEFAULT_VALUES[option]
        return a == "TRUE"
      elif (option.lower() in ("maxnum", "decimal_digits")):
        try:
          return int(setin["DEFAULT"][option])
        except (ValueError):
          if not WARN_IGNORE:
            cprint(f"[ERROR - saved settings] Invalid value: on the <{option}> option, please set a valid value as explained in the comments.", "light_red")
          return _DEFAULT_VALUES[option]
      else: return setin["DEFAULT"][option]
    except ( KeyError ):
      return _DEFAULT_VALUES[option]
  
  ENABLE_TIMER=get_settings("enable_timer")
  ISLOCAL=get_settings("isLocal")
  MAXNUM=get_settings("maxnum")
  DECIM_DIGS=get_settings("decimal_digits")
  RECORD_DISPLAY=get_settings("record_display")
except ( FileNotFoundError ): #set default value if there's no saved-settings at all
  ENABLE_TIMER=_DEFAULT_VALUES["enable_timer"]
  ISLOCAL=_DEFAULT_VALUES["isLocal"]
  MAXNUM=_DEFAULT_VALUES["maxnum"]
  DECIM_DIGS=_DEFAULT_VALUES["decimal_digits"]
  RECORD_DISPLAY=_DEFAULT_VALUES["record_display"]



OPRAN = {
  '+': lambda a, b: a + b, 
  '-': lambda a, b: a - b,
  '*': lambda a, b: a * b, 
  '/': lambda a, b: a / b,
}
def mathprob(m=0): #core code for the game
  n = [random.randint(1,MAXNUM) for x in range(2)]
  if(m==0):
    ot=random.choice(list(OPRAN.keys()))
    return n[0], n[1], ot, ( round(OPRAN[ot](n[0], n[1]), DECIM_DIGS) if DECIM_DIGS>0 else round(OPRAN[ot](n[0], n[1])) )