# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
# Custom table view.

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
import shutil
# pip install
import pandas as pd
from PyQt5.QtCore import ( Qt, pyqtSignal )
from PyQt5.QtWidgets import ( QMessageBox, QComboBox, QPushButton,
    QWidget, QGridLayout, QLineEdit )
# same project
from wristsaver.writing_type.PhysicalType import Columns as PhysicalTypeColumns
from wristsaver.common.pyqt5.PandasTableView import PandasTableView
from wristsaver.common.pyqt5 import set_actions, remove_actions

class OtoIniTable( PandasTableView ):
    
    # Custom table view.
    # Data in this table is set from the outside.
    
    def __init__( self,
                  physical_type_manager,
                  parent=None,
                  *args, **kwargs ):
        super( OtoIniTable, self ).__init__(
            parent=parent, *args, **kwargs )
        
        # appearance
        self.setWordWrap( False )
        self.setAcceptDrops(True)
        self.setContextMenuPolicy( Qt.ActionsContextMenu )
        
        # gui
        
        # interactions
        #self.__init_context_menu()
        
    def __init_context_menu( self ):
        
        # Called once during init.
        
        actions = [
             {
                 'text': 'Edit',
                 'method': self.edit_selection,
                 'shortcut': 'Alt+Return',
                 },
            ]
        
        set_actions( self, actions )
        
    def mouseDoubleClickEvent( self, ev ):
    
        if ev.button()==Qt.LeftButton:
            self.edit_selection()
            
    def edit_selection( self ):
        
        c = PhysicalTypeColumns
            
        df = self.get_df()
        seldf = self.selectedSubdf()
        
        mask = df[c.basename].isin( seldf[c.basename] )
        
        #df[mask]
            
#---------------------------------------------------------------------------+++
# end 2023.05.16
# separated into another file
