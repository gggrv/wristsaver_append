# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
#from shutil import rmtree, copytree
# pip install
# same project
from wristsaver.common import unique_loc
from wristsaver.common.SomeDoer import SomeDoer
from wristsaver.writing_type.PhysicalType import PhysicalType

class PhysicalTypeManager( SomeDoer ):
    
    # Allows to manage existing physical fonts.

    # for external use, may be ignored
    PREFERRED_SAVE_DIR_NAME = 'fonts'
    
    # future dictionary
    _generate_file_functions = None
    
    # future list
    __physical_types = None
    
    def __init__( self,
        save_folder
        ):
        
        super( PhysicalTypeManager, self ).__init__( save_folder )
        
        # dynamic
        self._generate_file_functions = {}
        self.__physical_types = []
        
        # autorun
        self._load()
        
    def get_available( self ):
        return self.__physical_types
    
    def get_specific( self, physical_type_name ):
        
        # Creates disposable physical type interface.
        
        # this physical type does not exist on disk yet
        if not physical_type_name in self.__physical_types:
            # add entry
            # no physical files are created yet though
            self.__physical_types.append( physical_type_name )
        
        # create object
        src = os.path.join( self.get_save_folder(), physical_type_name )
        pt_interface = PhysicalType( src )
        
        return pt_interface
    
    """
    def delete_specific( self, physical_type_name ):
        
        # TODO
        # do it safely
        
        if not physical_type_name in self.__physical_types:
            return
        
        # remove from disk
        src = os.path.join( self.get_save_folder(), physical_type_name )
        rmtree( src )
    
        # remove from list
        self.__physical_types.remove( physical_type_name )
    
    def duplicate_specific( self, physical_type_name ):
        
        # help:
        # https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
        
        # TODO
        # do it safely
        
        if not physical_type_name in self.__physical_types:
            return
        
        new_name = f'{physical_type_name}_{unique_loc()}'
        
        # copy
        src_from = os.path.join( self.get_save_folder(), physical_type_name )
        src_to = os.path.join( self.get_save_folder(), new_name )
        copytree( src_from, src_to )
    
        # add to list
        self.__physical_types.append( new_name )
        
        return new_name
    """
        
    def _load( self ):
        
        # Force reloads available physical type names.
        
        # clear existing
        self.__physical_types = []
        
        # get available font names
        for f in os.listdir( self.get_save_folder() ):
            self.__physical_types.append(f)

#---------------------------------------------------------------------------+++
# end 2023.05.16
# untested additional functions
