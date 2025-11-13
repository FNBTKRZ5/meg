"""
Basic math problems.
As alternative since I cant use tt rockstars DANGIT.
for framework: Bottle. (can't use Kivy because termux don't support GUI, so we'll use webpage.)

But first, gonna work with the algorithm first.
Basic arithmetics.
branch of mathematics / puzzle i wanted to add:
> Extreme addition
> Cryptarithm
> Limit
> Integral
> Statistic
> Series of numbers
> KPK & FPB

The settings is in a file named meg_stg.ini
"""
#preparing
import configparser
import re
from termcolor import cprint, colored
import time
from datetime import datetime as dt, date, timezone
import os
import json
from tabulate import tabulate
import signal as sg
import sys
import meg_f
import numpy as np


os.chdir(os.path.abspath(os.path.dirname(__file__))) #to avoid if it has the same issues regarding the working dir
setin=configparser.ConfigParser()
try:
  setin.read("meg_stg.ini") #the name of the file for saved settings is here!

  enable_timer=setin["DEFAULT"]["enable_timer"]
  isLocal=setin["DEFAULT"]["isLocal"]
  maxnum=int(setin["DEFAULT"]["maxnum"])
except:
  enable_timer=True
  isLocal=True
  maxnum=99

pl=True #to start the looping of the game until it stopped
tq=0 #number of question solved
tf=0 #number of failed attempts
if isLocal:
  strd="meg_score.json" #path to the saved score
  try:
    with open(strd) as f:
      trd = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    trd={}
# Register the handler with the SIGINT (Signal Interrupt or when CTRL+C is pressed) signal
def handle_exit(signum, frame):
  cprint("Alright!..\nStopping the program...", "red")
  sys.exit()
sg.signal(sg.SIGINT, handle_exit)


#the mathematics branches
opran = meg_f.opran  


#action
if(len(trd)==0):
  cprint(" you don't have any saved history to show. ", "magenta", "on_white")
else: #show leaderboard (if the data exist)
  besc=[]
  totalneeded=10
  for i in trd:
    t=trd[i].copy()
    t["datetime"]=i
    besc.append(t)
  hdr=["\033[38;5;214mRank\033[0m", colored("Time", "yellow"), colored("Time Record","light_red"), colored("TSolved", "light_green"), colored("Score", "light_magenta"), colored("cap", "light_blue")]
  
  if ( len(besc) > 1 ):
    necat = ["total_solved", "time_record", "score", "number_cap"]
    wecat = [0.95, 0.93, 0.92, 0.87]
    
    bt = np.array([[int(y[x]) if x!="time_record" else dt.combine(date(1970,1,1), dt.strptime(y[x], "%H:%M:%S.%f").time()).replace(tzinfo=timezone.utc).timestamp() for x in necat] for y in besc])
    bt = (bt - bt.min(axis=0))/(bt.max(axis=0)-bt.min(axis=0))
    bt[:, 1] = 1 - bt[:, 1]
    bt = bt @ np.array([x/sum(wecat) for x in wecat])
    for i, x in zip(besc, bt):
      i["combined_values"]=float(x)
    besc.sort(key=lambda x: -x["combined_values"])
  #ask user which mode to show leaderboard
  print("Choose the display mode to show the leaderboard")
  cprint("md [0] or normal [1]? (pick the index)", "yellow")
  
  deffmt="grid"
  tablefmtopt=input(">")
  tablefmtopt= "pipe" if tablefmtopt=="0" else "grid" if tablefmtopt=="1" else deffmt
  
  cprint(f"Your TOP {totalneeded} Records", "light_blue", "on_white")
  print(tabulate([[i+1, v["datetime"], v["time_record"], v["total_solved"], v["score"], v["number_cap"]] for i,v in enumerate(besc)][0:totalneeded], headers=hdr,tablefmt=tablefmtopt, colalign=("center", "center", "center", "center","center")), "\n")


#waits for the user to start the game
enterornot=input("Press [ENTER] to start..!  "+colored("or Press [CTRL]+C or any elm to exit.", "dark_grey"))
if (len(enterornot)):
  cprint("jusf want to peek, huh?\nalrighty, cya!\n\n", "light_red")
  sys.exit()
print(".\n.\n.\n") #just a divider
if(enable_timer):
  tmr = time.time() #start a timer
  cdt=dt.now()
nitr=1 #question index
while(pl):
  n1, n2, op, res=meg_f.mathprob() #generate problems
  print(f"{nitr}.]  {n1} {op} {n2} = ?")
  while(True): #loop until answer is correct
    try:
      usr=re.sub("\\s", "", input("Your answer: "))
      if(len(usr)==0): #quit/stop immediately if empty
        conf=input(colored("Type anything to confirm your exits then press [ENTER]! :)\n*the time still running even when you're here.", "light_yellow"))
        if(conf):
          pl=False
        else: continue
      elif(float(usr)!=res):
        tf+=1 #increment of the failed attempt
        continue
      elif(float(usr)==res): tq+=1 #question is solved
      break
    except ValueError:
      cprint("Number Only.", "light_red")
  nitr+=1

if(enable_timer): #stopwatch
  et = time.time() - tmr
  hr,mins,secs=0,0,0
  if(et//3600!=0): #if it contains at least an hour
    hr=int(et//3600)
    mins=int((et%3600)//60)
    secs=(et%3600)%60
  elif(et//60!=0): #if it contains at least a minute
    mins=int(et//60)
    secs=et%60
  else: secs=et
  secs=round(secs,3)
if(tq==0): #if no question is solved
  scr="N/A"
  cprint("Score is invalid because you didn't finish solving any question.", "light_red")
else: scr=round((tq-tf)/tq*100,1)
#result of the session
cprint(f"""Oh!.. Okay.
Today's date is {date.today()}
Here's your score: {scr}
You failed: {tf} time(s)
You solved: {tq} problem(s)""", "cyan")
if(enable_timer):
  cprint(f"You did it in {hr:02}:{mins:02}:{secs:06.3f} !", "cyan")
elif(scr>95):
  cprint("Ayy that's such score! You should challenge yourself and do it with a timer >:D")
if(tq!=0):
  usr=input("want to save your score? [Y?]\n*Skipping or anything outside the option will cancel this action.\n>").lower()
  if(usr=="y"):
    cdt=dt.now().strftime("%d/%m/%y")
    if cdt in trd and not (cdt+" (2)" in trd): # if this is the second attempt on the same day
      cdt+=" (2)"
      print("2")
    elif cdt+" (2)" in trd: #if more than 2 attempts
      b=[]
      for i in trd.items():
        a=re.search("\\(\\d+\\)$", i[0])
        if a:
          b.append(re.sub("[\\(\\)]", "", a.group()))
      cdt+=" ("+str(int(max(b))+1)+")"
    trd.update({cdt: {
        "time_record": f"{hr:02}:{mins:02}:{secs:06.3f}",
        "total_solved": tq,
        "score": scr,
        "number_cap": maxnum
      }})
    if isLocal:
      with open(strd, "w+") as f:
        json.dump(trd, f, indent=2, separators=(",",": "))
      print("Has been saved locally!")