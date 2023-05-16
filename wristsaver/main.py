# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
# same project
from wristsaver.common.SomeDoer import SomeDoer
    
class Paths:
    
    __CODE_ROOT = os.path.dirname( __file__ )
    __APPLICATION_ROOT = os.path.dirname( __CODE_ROOT )
    __DATA_ROOT = os.path.join( __APPLICATION_ROOT, 'data' )
    
    # provides access to data folder
    __own_doer = None
    
    @staticmethod
    def get_code_root():
        # Returns the root folder of the main code.
        return Paths.__CODE_ROOT
    
    @staticmethod
    def get_application_root():
        # Returns the root folder of this application.
        return Paths.__APPLICATION_ROOT
    
    @staticmethod
    def get_data_root():
        # Returns the root folder of the user
        # customizeable data folder
        # that is managed by __MasterDoer.
        return Paths.__DATA_ROOT
    
    @staticmethod
    def __get_data_manager():
        
        # For internal use only.
        
        # make sure it exists
        if( Paths.__own_doer is None ):
            
            Paths.__own_doer = SomeDoer(
                Paths.__DATA_ROOT
                )
            
        return Paths.__own_doer
        
    @staticmethod
    def set_file( filename ):
        
        # Sets file inside the data folder.
        
        Mgr = Paths.__get_data_manager()
        
        src = Mgr.set_file( filename )
        
        return src
        
    @staticmethod
    def set_folder( dirname ):
        
        # Sets folder inside the data folder.
        
        Mgr = Paths.__get_data_manager()
        
        src = Mgr.set_folder( dirname )
            
        return src

#---------------------------------------------------------------------------+++
# end 2023.05.14
# simplified
