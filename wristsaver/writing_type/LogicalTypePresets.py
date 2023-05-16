# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
# pip install
# same project
from wristsaver.common.PresetManager import PresetManager
    
class Columns:
    
    SCREEN_NAME = 'screen_name'
    DERIVE_FROM = 'physical_type_name'
    
    SCALE = 1 # float amount
    TILT = 0 # degrees
    WEIGHT = 0
    KERN_X = 0 # move right
    KERN_Y = 0 # move up
    LETTER_SPACING = 0 # float
    
class LogicalTypePresets( PresetManager ):
    
    # Creates different preset settings for physical fonts.
    # These settings define logical fonts derived from physical ones.
    
    Columns = Columns
    
    def __init__( self, file_name ):
        
        super( LogicalTypePresets, self ).__init__( file_name )
        
    def get_dictionary( self, keys=None ):
        
        ps = self.get_presets()
        
        if keys is None: keys=ps.keys()
        
        result = {}
        for unique_name, p in ps.items():
            for k in keys:
                result[unique_name] = p[k]
                
        return result
        
    def new_preset(
            self,
            unique_name,
            screen_name,
            derive_from,
            scale,
            tilt,
            weight,
            kern_x,
            kern_y,
            letter_spacing
            ):
        
        # Saves preset.
        
        c = Columns
        
        # add new
        
        row = {
            c.SCREEN_NAME: screen_name,
            c.DERIVE_FROM: derive_from,
            c.SCALE: scale,
            c.TILT: tilt,
            c.WEIGHT: weight,
            c.KERN_X: kern_x,
            c.KERN_Y: kern_y,
            c.LETTER_SPACING: letter_spacing
            }
            
        if self._presets is None:
            # im creating first preset ever
            
            self._presets = {
                unique_name: row
                }
            
        else:
            # im adding new / replacing same existing
            self._presets[unique_name] = row
            
        self._save_all_presets()

#---------------------------------------------------------------------------+++
# end 2023.05.14
# created
