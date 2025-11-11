import random
import configparser
import os

os.chdir(os.path.abspath(os.path.dirname(__file__))) #to avoid incoming issue regarding working dir
setin=configparser.ConfigParser()
try:
  setin.read("meg_stg.ini")
  
  maxnum=int(setin["DEFAULT"]["maxnum"])
  decim_digs=int(setin["DEFAULT"]["decimal_digits"])
except (FileNotFoundError, KeyError): #set default value if there's no saved-settings
  maxnum=99
  decim_digs=0

opran = {
  '+': lambda a, b: a + b, 
  '-': lambda a, b: a - b,
  '*': lambda a, b: a * b, 
  '/': lambda a, b: a / b,
}
def mathprob(m=0): #core code for the game
  n = [random.randint(1,maxnum) for x in range(2)]
  if(m==0):
    ot=random.choice(list(opran.keys()))
    return n[0], n[1], ot, ( round(opran[ot](n[0], n[1]), decim_digs) if decim_digs>0 else round(opran[ot](n[0], n[1])) )