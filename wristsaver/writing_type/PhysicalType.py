# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
import pandas as pd
# same project
from wristsaver.common.SomeDoer import SomeDoer

class Columns:
    
    # which filename does this picture have
    basename = 'basename'
    
    # which text does it contain
    text = 'text'
    
    # coordinates of the upper left corner
    crop_x1 = 'crop_x1'
    crop_y1 = 'crop_y1'
    # coordinates of the lower right corner
    crop_x2 = 'crop_x2'
    crop_y2 = 'crop_y2'
    
    # which symbols are ok/not allowed to precede/follow
    # this one
    allow_left = 'ok_left'
    allow_right = 'ok_right'
    forbid_left = 'no_left'
    forbid_right = 'no_right'
    
    # for programming use only
    SRC = 'src'
    
    # may be useful
    _SAVEABLE_COLUMNS = [
        basename,
        text,
        crop_x1,
        crop_y1,
        crop_x2,
        crop_y2,
        allow_left,
        allow_right,
        forbid_left,
        forbid_right
        ]

def files_to_oto( basenames ):
    
    c = Columns
    
    rows = []
    for basename in basenames:
        
        #basename = os.path.basename(src)
        name, _ = os.path.splitext( basename )
        
        row = {
            
            c.basename: basename,
            c.text: name,
            
            c.crop_x1: 0,
            c.crop_y1: 0,
            c.crop_x2: 0,
            c.crop_y2: 0,
            
            }
        
        rows.append( row )
        
    df = pd.DataFrame( rows )
    
    df[c.allow_left] = None
    df[c.allow_right] = None
    df[c.forbid_left] = None
    df[c.forbid_right] = None
    
    return df

class PhysicalType:
    
    # An interface to some font that resides on disk.

    Columns = Columns
    
    # top directory with font data
    __ROOT_FOLDER = None # future path
    
    __BASENAME = None
    
    _df = None
    
    class Files:
        
        OTO_INI = 'index.csv'
        
    def __init__( self, root_folder ):
        
        self.__ROOT_FOLDER = root_folder
        self.__BASENAME = os.path.basename(self.__ROOT_FOLDER)
        
    def df( self ):
        
        if self._df is None:
            self._df = self._load()
            
        return self._df
    
    def basename( self ):
        
        return self.__BASENAME
        
    def _load( self ):
        
        # Parses root folder, constructs one oto.ini
        # from multiple ones.
        # If oto does not exist, creates it.
        # If it already exists (maybe it was edited by human), reads it.
        
        c = Columns
        OTO_INI = PhysicalType.Files.OTO_INI
        
        dfs = []
        for root, subs, files in os.walk( self.__ROOT_FOLDER ):
            
            # this loop runs for each subfolder
            # including root
            
            if len(files)==0:
                # no files in this subfolder
                # nothing to do
                continue
            
            src = os.path.join( root, OTO_INI )
            
            if OTO_INI in files:
                # this is the thing i want to load
                df = pd.read_csv(src)
                #if len(files)==1:
                #    # no other files, ???
                #    continue
            else:
                # i lack oto.ini in this subfolder, create it
                df = files_to_oto( files )
                df.to_csv( src, index=False )
            
            # add full paths
            df[c.SRC] = [ os.path.join(root,f) for f in df[c.basename] ]
            dfs.append( df )
            
        # TODO
        # add file extension filter
        
        if len(dfs)==0:
            return pd.DataFrame( columns=Columns._SAVEABLE_COLUMNS )
        
        df = pd.concat( dfs, axis=0, sort=False )
        return df

#---------------------------------------------------------------------------+++
# end 2023.05.16
# update
