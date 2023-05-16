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
from wristsaver.pyqt5.OtoIniTable import OtoIniTable
from wristsaver.common.pyqt5 import set_actions, remove_actions
        
class PhysicalTypeEditor( QWidget ):
    
    # Overarching container widget
    # with various controls.
    
    class Gui:
        
        existing_cbx = None
        #bt_new = None
        #bt_delete = None
        #bt_duplicate = None
        
        table_view = None
    
    __physical_type_manager = None
    __current_pt_interface = None

    def __init__( self,
                  physical_type_manager,
                  parent=None,
                  *args, **kwargs ):
        super( PhysicalTypeEditor, self ).__init__(
            parent=parent, *args, **kwargs )
        
        self.__physical_type_manager = physical_type_manager
        
        # gui
        
        self.Gui.existing_cbx = QComboBox( parent=self )
        self.Gui.existing_cbx.currentTextChanged.connect( self.__physical_type_changed_event )
        #self.Gui.bt_new = QPushButton( 'New', parent=self )
        #self.Gui.bt_new.clicked.connect( self.__add_new_event )
        #self.Gui.bt_delete = QPushButton( 'Delete', parent=self )
        #self.Gui.bt_delete.clicked.connect( self.__delete_current_event )
        #self.Gui.bt_duplicate = QPushButton( 'Duplicate', parent=self )
        #self.Gui.bt_duplicate.clicked.connect( self.__duplicate_current_event )
        
        self.Gui.table_view = OtoIniTable( self.__physical_type_manager )
        
        # assemble
        
        lyt = QGridLayout()
        
        rowiloc = 0
        span = 2
        lyt.addWidget( self.Gui.existing_cbx, rowiloc,0, 1,span  )
        
        rowiloc = 1
        lyt.addWidget( self.Gui.table_view, rowiloc,0 )
        
        self.setLayout( lyt )
        
        # autorun
        
        # trigger refill
        self.Gui.existing_cbx.addItems( self.__physical_type_manager.get_available() )
        
    def __physical_type_changed_event( self ):
        
        # Change displayed contents.
        
        physical_type_name = self.Gui.existing_cbx.currentText()
        
        # is it already loaded?
        if not self.__current_pt_interface is None:
            if self.__current_pt_interface.basename()==physical_type_name:
                # no change
                return
        
        # create new interface
        # while discarding previous one in the process
        pt_interface = self.__physical_type_manager.get_specific( physical_type_name )
        self.__current_pt_interface = pt_interface
        
        # show it
        self.Gui.table_view.switch_df( self.__current_pt_interface.df() )
        
    """
    def __add_new_event( self ):
        
        pass
        
    def __delete_current_event( self ):
        
        unique_name = self.Gui.existing_cbx.currentText()
        if unique_name == '':
            return
        
        new_name = self._physical_type_manager.duplicate_specific( unique_name )
        
        # append to cbx
        self.Gui.cbx.addItem( new_name )
        
        # automatically load it 
        #self.Gui.cbx.setCurrentIndex( self.Gui.cbx.count()-1 )
        
    def __duplicate_current_event( self ):
        
        unique_name = self.Gui.existing_cbx.currentText()
        if unique_name == '':
            return
    """
            
#---------------------------------------------------------------------------+++
# end 2023.05.16
# created
