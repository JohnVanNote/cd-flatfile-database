#!/usr/bin/python
#
# album.py
#
# Class for Album Object
#
# Created by John Van Note
# Created on 12/01/2011
#

class album(object):
  
  # constructor: Initializes album class
  # @param name is a string album name
  # @param year is an int for the release year of the album
  # @param art is a string for the artist of the album
  # @param tracks is a list of the album tracks
  # no return
  def __init__(self, name, year, art, tracks):
    self.nm_ = name
    self.yr_ = year
    self.art_ = art
    self.trx_ = tracks

  # display:Displays a album in a specialized format for the database file
  # @return a list of strings for the file
  def display(self):
    display = []
    display.append(self.art_)
    display.append(str(self.yr_) + " " + self.nm_)
    for track in self.trx_:
      display.append("-" + track)
    return display
  
  # getArt: gets the artist 
  # @return artist of album (string)
  def __getArt__(self):
    return self.art_

  # getName: gets the name 
  # @return name of album (string)
  def __getName__(self):
    return self.nm_

  # getYear: does what you think it does
  # @return year of album (int)
  def __getYear__(self):
    return self.yr_

#eof
