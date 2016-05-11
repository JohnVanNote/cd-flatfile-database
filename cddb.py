#!usr/bin/python
#
# cddb.py
#
# Creates a cd database with option to:
# - Display the database
# - Add an album
# - Delete an album
# - Usage message
#
# Created by John Van Note
# Created on 12/01/11
#

import sys
import os.path
import shutil
import array
from album import *

data = "cddb.db" 
temp = "cddb.tmp"

# l: Displays current albums in the database
# displays artists first, allows user to choose
# displays albums of chosen artist
# displays songs of chosen albums
# no return
def l():
  check = open( data, "r" )
  size = check.readlines()
  size = len( size )
  if size < 2:
    print "Cannot list an empty database"
    sys.exit()
  print "FOR VIEW"
  chArt = chooseArt( data ) 
  print "FOR VIEW"
  chAlb = chooseAlb( data, chArt )
  trx = trxList( data, chArt, chAlb )
  for track in trx:
    print track
  chTrx = raw_input( "Enter \'r\' to return to the previous menu, \'q\' to quit: " )
  if chTrx == "r" or chTrx == "return":
    chooseAlb(data, chArt )

# a: Adds an album to the database
# if the database is empty, this will create a database
# validates user input
# does not add an existing album
# artist & album name are case sensitive
# no return
def a():
  print data
  newAlbum = getInput()
  if os.path.isfile( data ):
    appendDb( data, temp, newAlbum )
  else:
    createDb(  data, temp, newAlbum )
  shutil.copy2( temp, data )
  os.remove( temp )

# d: Deletes an album from the database
# Based on user choice
# Similar to l() function
# no return
def d():
  check = open( data, "r" )
  size = check.readlines()
  size = len( size )
  if size < 2:
    print "Cannot delete from an empty list"
    sys.exit()
  print "FOR DELETION"
  chArt = chooseArt( data )
  print "FOR DELETION"
  chAlb = chooseAlb( data, chArt )
  deleteAlb( data, temp, chArt, chAlb )
  shutil.copy2( temp ,data ) 
  os.remove( temp )

# h: Explains usage for the cddb utility
# then exits, no user interaction required
# no return
def h():
  print "\nThe cddb is a utility that keeps a flat file database of cd entries"
  print "\nOptions: "
  print "\t -l, --list-album\tDisplays a list of albums"
  print "\t -d, --delete-album\tDeletes album entry from database"
  print "\t -a, --add-album\tAdds album entry to database"
  print "\t -h, --usage\t\tDisplays use message and quits utility"

# getInput: Gets user input regarding adding an album
# @return album (data type)
def getInput():
  artist = raw_input( "Artist: " )
  name = raw_input( "Album name: " )
  year = int( raw_input( "Year released (ex. 1999): " ))
  tracks = []
  i = 0
  print "Enter track names, \'d\' when complete: "
  tracks.append( raw_input( "... " ))
  while( tracks[i] != "d" ):
    tracks.append( raw_input( "... " ))
    i += 1
  tracks.remove( "d" )
  newAlbum = album( name, year, artist, tracks )
  print "\nIs the following information correct?"
  display = newAlbum.display()
  for lines in display:
   print lines
  resp = raw_input( "Enter \'y\' to continue or \'q\' to quit: " )
  if resp != "y" and resp != "yes" and resp != "q" and resp != "quit" :
    return getInput()
  elif resp == "q" or resp == "quit":
    sys.exit()
  return newAlbum

# createDb: Creates a database for album
# @param src is the file to be written
# @param dist is the temporary file to be tested
# @param alb is the album to be added
# no return
def createDb( src, dist, alb ):
  new_file = open( dist, "w" )
  old_file = open( src, "w" )
  old_file.close()
  for lines in alb.display():
    new_file.write(lines + "\n")
  new_file.write( "\n" )
  new_file.close()

# appendDb: Appends an existing database with new albums
# checks for an existing album
# @param src is the file to be written
# @param dist is the temporary file to be tested
# @param alb is the album to be added
# no return
def appendDb( src, dist, alb ):
  new_file = open( dist, "w" )
  old_file = open( src, "r" )
  old_data = old_file.readlines()
  old_file.close()
  act_art = alb.__getArt__()
  act_nm = str( alb.__getYear__() ) + " " + alb.__getName__()
  i = 0
  for lines in old_data:
    if i != len(old_data)-1:
      poss_art = rmvN( old_data[i] )
      poss_nm = rmvN( old_data[i+1] )
      if act_art == poss_art and act_nm == poss_nm:
        print "Album already in database"
        sys.exit()
    new_file.write( lines )
    i += 1
  for lines in alb.display():
    new_file.write(lines + "\n")
  new_file.write( "\n" )
  new_file.close()

# artDict: Finds artists and the albums for each artist in the databae
# @param src is the datafile with information
# @return a dictionary with key artist to their albums
def artDict( src ):
  lib = {}
  read_file = open( src, "r" )
  data = read_file.readlines()
  f_key = rmvN( data[0] )
  f_val = rmvN( data[1] )
  lib[ f_key ] = f_val + "\n"
  i = 0
  for lines in data:
    if lines == "\n" and i != len(data)-1:
      n_key = rmvN( data[i+1] )
      n_val = rmvN( data[i+2] )
      if lib.has_key( n_key ):
        o_val = lib.get( n_key )
        o_val = o_val  + n_val + "\n"
        lib[ n_key ] = o_val
      else:
        lib[ n_key ] = n_val + "\n"
    i += 1
  read_file.close()
  return lib

# trxList: Looks into the database files, finds tracks for a specific cd
# @param src is the database file
# @param artName is a string for the name of the artist
# @param albName is a stirng for the name of the album
# @return list of strings for tracks of the album
def trxList( src, artName, albName ):
  trx = []
  read_file = open( src, "r" )
  data = read_file.readlines()
  i = 0
  for lines in data:
    if i != len(data)-1:    
      poss_art = rmvN( data[i] )
      poss_alb = rmvN( data[i+1] )
      if poss_art != artName :
        pass
      elif poss_alb != albName :
        pass
      else:
        j = i+2
        while data[j] != "\n":
          track = rmvN( data[j] )
          trx.append( track )
          j += 1
    i += 1
  read_file.close() 
  return trx

# deleteAlb: Deletes an album from the database
# @param src is the database source file
# @param dist is the temp file to be tested
# @param artName is a string for the name of the artist
# @param albName is a strign for the name of the album
# no return
def deleteAlb( src, dist, artName, albName ):
  new_file = open( dist, "w" )
  old_file = open( src, "r" )
  data = old_file.readlines()
  old_file.close()
  i = 0
  while i < len(data):
    poss_art = rmvN( data[i] )
    if poss_art == artName:
      poss_nm = rmvN( data[i+1] )
      if poss_nm == albName:
        while data[i] != "\n":
          i += 1
      else:
        new_file.write( data[i] )
        i += 1
    else:
      new_file.write( data[i] )
      i += 1
  new_file.close()
  cleanUp( dist )

# cleanUp: Cleans up extra lines in a file
# @param src is the source file
# no return
def cleanUp( src ):
  dirty_file = open( src, "r" )
  dirty_data = dirty_file.readlines()
  dirty_file.close()
  os.remove( src )
  clean_file = open( src, "w" ) 
  if dirty_data[0] == "\n":
    i = 1
  else:
    i = 0
  while i < len(dirty_data)-1:
    if dirty_data[i] == "\n" and dirty_data[i+1] == "\n":
      i += 1
    clean_file.write( dirty_data[i] )
    i += 1
  if dirty_data[i-1] != "\n":
    clean_file.write( "\n" )
  clean_file.close()

# bufferEntry: Takes the string of alb names and splits them if entry has multiple albums
# @param entry is a string with newlines to seperate strings
# @return a list of strings without newlines
def bufferEntry( entry ):
  newEntry = entry.split( "\n" )
  newEntry.pop() # gets rid of last blank entry
  return newEntry

# chooseArt: Provide list of artists in database for user
# allows user to choose which artist or quit
# @param src is the database file for cds
# @return the integer of the choice
def chooseArt(src):
  list_art = artDict( src )
  art_keys = list_art.keys()
  art_keys.sort()
  i = 0
  for arts in art_keys:
    print str(i) + " : " + arts
    i += 1
  choice = raw_input( "\nChoose a # from the list, or enter \'q\' to quit: " )
  if choice == "q" or choice == "quit":
    sys.exit()
  elif 0 <= int( choice ) <= i:
    return art_keys[ int( choice ) ]
  else:
    print "Input invalid, please try again"
    return chooseArt( src )

# chooseAlb: Provides a list of albums from specific artist for the user to choose
# gives user opportunity to go back to chooseArt() func
# @param src is the database file for cd's
# @param artName is the string of the artist name chosen by the user
# @return string of cd name
def chooseAlb( src, artName ):
  list_art = artDict( src )
  allAlbs = list_art.get( artName )
  newAlbs = bufferEntry( allAlbs )
  newAlbs.sort()
  i = 0
  for albs in newAlbs:
    print str( i ) + " : " + albs
    i += 1
  choice = raw_input( "\nChoose a # from the list, or enter \'a\' to return to artists: " )
  if choice == "a" or choice == "artists":
    chooseArt(src)
  elif 0 <= int( choice ) <= i:
    return newAlbs[int( choice )]
  else:
    print "Input invalid, please try again"
    return chooseAlb( src, artName )  

# rmvN: Removes newspace from a string
# @param s is a string ending in a newspace (\n)
# @return string without newspace
def rmvN(s):
  s = s.strip( "\n" )
  return s

# main program
def main():
  EXT = sys.argv[1]
  if EXT == "a":
    a()
  elif EXT == "d":
    d() 
  elif EXT == "l":
    l()
  elif EXT == "h":
    h()
  else:
    print "Invalid Argument"

# ensures the program is run correctly
if __name__ == "__main__":
  main()

#eof
