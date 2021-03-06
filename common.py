# bunch of functions from MMlib
opt={'no_colors':0, 'Q':0}
colored_keywords={}
printed_rchar=0
from string import lowercase, uppercase, digits #, lower, upper
import sys
from copy import deepcopy
from  colorsys import hsv_to_rgb, rgb_to_hsv
import pandas as pd
from hashlib import md5

import os
def mute(also_stderr=False):
  """ Turns off any output to stdout (to stderr as well if option is True). To go back to normal , use unmute()"""
  sys.stdout = open(os.devnull, "w")
  if also_stderr:   sys.stderr = open(os.devnull, "w")

def unmute():
  sys.stdout = sys.__stdout__;  sys.stderr = sys.__stderr__


def md5_of_dataframe(df):
  m = md5()
  if isinstance(df, pd.Series):   m.update( df.to_msgpack() )
  else: 
    for row_i in df.index:        m.update(  df.loc[row_i].to_msgpack()    )
  return m.digest()

class NodeSelector(set):
  """ """
  def walk_tree(self, up=False, down=False, only_ancestors=False, only_leaves=False, maxup=None, maxdown=None):
    """Return a NodeSelector with all nodes that you would encounter going up to the root and/or down to leaves  (depending on arguments up and down) starting from any of the nodes in this self NodeSelector."""
    out=NodeSelector()
    for n in self:
      if down:
        for level, d in n.traverse_by_level(exclude_fn=lambda x:x in out):
          #print d
          if level==0: continue
          #if d in out: exclude.add(d); continue
          out.add(d)
          if not maxdown is None and level==maxdown:   break          
      if not n in out and (not only_ancestors or not n.is_leaf()): out.add(n) 
      if up:
        u=n;  upindex=0
        while u.up and not u.up in out: 
          out.add(u.up)        
          u=u.up
          upindex+=1
          if not maxup is None and upindex==maxup:     break

    if only_leaves: out= NodeSelector([n for n in out if n.is_leaf()])
    return out

def rescale(x, ymin, ymax, xmin=0.0, xmax=1.0):  
  """Generic function to compute proportions; it rescales proportionally an 
  input x, which is between xmin and xmax, to output y, which is between ymin and ymax """
  return ymin + (ymax-ymin) * ( (x-xmin)/(xmax-xmin) ) 

terminal_codes={'':'\033[0m', 'red':'\033[31m', 'green':'\033[32m', 'black':'\033[30m', 'yellow':'\033[33m', 'blue':'\033[34m', 'magenta':'\033[35m', 'cyan':'\033[36m', 'white':'\033[37m', 'bright':'\033[1m', 'dim':'\033[2m', 'underscore':'\033[4m', 'blink':'\033[5m', 'reverse':'\033[7m', 'hidden':'\033[8m'}

def printerr(msg, put_newline=0, how='', keywords={}, is_service=False):
  global printed_rchar
  if not keywords and colored_keywords: keywords=colored_keywords
  msg=str(msg)
  if put_newline:    msg=msg+'\n'
  no_color_msg=msg
  if printed_rchar:
    sys.stderr.write('\r'+printed_rchar*' '+'\r' )
    printed_rchar=0
  if sys.stdout.isatty() and not opt['no_colors']:
    if how:
      for c in how.split(','): 
        if not terminal_codes.has_key(c): raise Exception, "ERROR option 'how' for write was not recognized: "+str(c)+' ; possible values are: '+join([i for i in terminal_codes.keys() if i], ',')
        msg=terminal_codes[c]+msg+terminal_codes['']
    for word in keywords:
      code=''
      for c in keywords[word].split(','): code+=terminal_codes[c]
      msg= replace(msg, word, code+word+terminal_codes[''])
  sys.stderr.write(str(msg))
  if not is_service and 'log_file' in globals(): print >> log_file, str(no_color_msg),
  
def service(msg):
  """ see write function"""
  msg=str(msg)
  global printed_rchar, opt
  if sys.stderr.isatty() and  not opt['Q']:
    if printed_rchar:
      printerr('\r'+printed_rchar*' ', is_service=True )
    printerr( "\r"+msg, is_service=True)
    printed_rchar=len(msg)
  #if 'log_file' in globals(): print >> log_file, str(msg+'\n') #putting a newline

def verbose(msg, put_newline=0):
  global opt
  if put_newline:    msg=str(msg)+'\n'  
  if opt['v']:
    write( msg )
    if 'log_file' in globals(): print >> log_file, str(msg),
    
def write(msg, put_newline=0, how='', keywords={}):
  """ Function to extend the functionalities of the standard 'print'. First argument (put_newline) when set to 1 put a newline after the string passed, as print would normally do. The argument "how" can be given a color to write the message in that color (only for atty terminals). This is prevented if opt['no_colors'] is active.  The function write is coupled with function "service" which prints service message which are deleted when another service message is printed, or another message is printed with the write function. If you use service, you should only print things with "write".
Argument keywords allows to use certain colors (or other "how" arguments) for certain keywords. The argument is a hash of keywords and correspoding how arguments. for example if you want to higlight all "ERROR" in red, pass keywords={'ERROR':'red'} 
"""
  msg=str(msg)
  global printed_rchar, opt
  if not keywords and colored_keywords: keywords=colored_keywords
  if put_newline:     msg=msg+'\n'
  no_color_msg=msg
  if sys.stdout.isatty() and not opt['no_colors']:
    if how:
      for c in how.split(','): 
        if not terminal_codes.has_key(c): raise Exception, "ERROR option 'how' for write was not recognized: "+str(c)+' ; possible values are: '+join([i for i in terminal_codes.keys() if i], ',')
        msg=terminal_codes[c]+msg+terminal_codes['']
    for word in keywords:
      code=''
      for c in keywords[word].split(','): code+=terminal_codes[c]
      msg= replace(msg, word, code+word+terminal_codes[''])
  if printed_rchar:
    sys.stderr.write('\r'+printed_rchar*' '+'\r' )
    printed_rchar=0
  sys.stdout.write(msg)
  if 'log_file' in globals(): print >> log_file, no_color_msg, 
warning=write
