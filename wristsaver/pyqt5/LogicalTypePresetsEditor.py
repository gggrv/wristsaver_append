# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
# pip install
import pandas as pd
from PyQt5.QtCore import pyqtSignal, Qt, QModelIndex
from PyQt5.QtWidgets import (
    QWidget, QMessageBox, QComboBox, QTableWidgetItem, QGridLayout,
    QPushButton, QLineEdit, QLabel
    )
# same project
from wristsaver import MainPaths
from wristsaver.common import unique_loc
from wristsaver.common.pyqt5 import set_actions, remove_actions
from wristsaver.writing_type.LogicalTypePresets import LogicalTypePresets
        
class LogicalTypePresetsEditor( QWidget ):
    
    # GUI editor for LogicalTypePresets.
    
    physical_type_manager = None
    
    class Files:
        
        LOGICAL_TYPES = 'logical_fonts.yaml'
        
    class Presets:
        
        LogicalType = None
        
    # future dictionary
    __cached_screen_names = None
        
    class Gui:
        
        logical_types_cbx = None
        
        physical_types_lab = None
        physical_types_cbx = None
        
        screen_name_line = None
        
        scale_lab = None
        scale_inp = None
        
        tilt_lab = None
        tilt_inp = None
        
        weight_lab = None
        weight_inp = None
        
        kern_x_lab = None
        kern_x_inp = None
        
        kern_y_lab = None
        kern_y_inp = None
        
        letter_spacing_lab = None
        letter_slacing_inp = None
        
        # TODO
        # add auto-updating preview canvas
        
    def __init__( self,
                  physical_type_manager,
                  parent=None,
                  *args, **kwargs ):
        super( LogicalTypePresetsEditor, self ).__init__( parent=parent, *args, **kwargs )

        # remember
        self.physical_type_manager = physical_type_manager

        # paths
        self.Files.LOGICAL_TYPES = MainPaths.set_file( self.Files.LOGICAL_TYPES )

        # presets
        self.Presets.LogicalType = LogicalTypePresets( self.Files.LOGICAL_TYPES )
        
        self.setMaximumWidth( 550 )
        
        # gui
        
        c = self.Presets.LogicalType.Columns
        
        lyt = QGridLayout()
        
        # exiting logical presets selector
        self.__cached_screen_names = self.Presets.LogicalType.get_dictionary( [c.SCREEN_NAME] )
        self.Gui.logical_types_cbx = QComboBox( parent=self )
        self.Gui.logical_types_cbx.addItems( list( self.__cached_screen_names.values() ) )
        bt_load = QPushButton( 'Load', parent=self )
        bt_load.clicked.connect( self.bt_load )
        bt_clear = QPushButton( 'Clear All', parent=self )
        bt_clear.clicked.connect( self.bt_clear )
        
        # custom name
        self.Gui.screen_name_line = QLineEdit( parent=self )
        self.Gui.screen_name_line.setPlaceholderText( 'Custom Logical Font Name' )
        bt_save = QPushButton( 'Save', parent=self )
        bt_save.clicked.connect( self.bt_save )
        bt_delete = QPushButton( 'Delete', parent=self )
        bt_delete.clicked.connect( self.bt_delete )
        
        # derive from physical
        self.Gui.physical_types_lab = QLabel( 'Derives from physical font', parent=self )
        self.Gui.physical_types_cbx = QComboBox( parent=self )
        self.Gui.physical_types_cbx.addItems( self.physical_type_manager.get_available() )
        
        # settings
        
        self.Gui.scale_lab = QLabel( 'Scaling', parent=self )
        self.Gui.scale_inp = QLineEdit( parent=self )
        self.Gui.scale_inp.setText( '1' )
        
        self.Gui.tilt_lab = QLabel( 'Tilt (italic)', parent=self )
        self.Gui.tilt_inp = QLineEdit( parent=self )
        self.Gui.tilt_inp.setText( '0' )
        
        self.Gui.weight_lab = QLabel( 'Weight (bold)', parent=self )
        self.Gui.weight_inp = QLineEdit( parent=self )
        self.Gui.weight_inp.setText( '1' )
        
        self.Gui.kern_x_lab = QLabel( 'Shift X +- →←', parent=self )
        self.Gui.kern_x_inp = QLineEdit( parent=self )
        self.Gui.kern_x_inp.setText( '0' )
        
        self.Gui.kern_y_lab = QLabel( 'Shift Y +- ↑↓', parent=self )
        self.Gui.kern_y_inp = QLineEdit( parent=self )
        self.Gui.kern_y_inp.setText( '1' )
        
        self.Gui.letter_spacing_lab = QLabel( 'Additional letterspacing', parent=self )
        self.Gui.letter_spacing_inp = QLineEdit( parent=self )
        self.Gui.letter_spacing_inp.setText( '0' )
        
        # assemble
        
        # widget, cells, span
        
        rowiloc = 0
        spanx = 2
        lyt.addWidget( self.Gui.logical_types_cbx, rowiloc,0, 1,spanx )
        lyt.addWidget( bt_load, rowiloc,spanx+1 )
        lyt.addWidget( bt_clear, rowiloc,spanx+2 )
        
        rowiloc = 1
        spanx = 2
        lyt.addWidget( self.Gui.screen_name_line, rowiloc,0, 1,spanx )
        lyt.addWidget( bt_save, rowiloc,spanx+1 )
        lyt.addWidget( bt_delete, rowiloc,spanx+2 )
        
        rowiloc = 2
        lyt.addWidget( self.Gui.physical_types_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.physical_types_cbx, rowiloc,spanx+1, 1,spanx )
        rowiloc = 3
        lyt.addWidget( self.Gui.scale_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.scale_inp, rowiloc,spanx+1, 1,spanx )
        rowiloc = 4
        lyt.addWidget( self.Gui.tilt_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.tilt_inp, rowiloc,spanx+1, 1,spanx )
        rowiloc = 5
        lyt.addWidget( self.Gui.weight_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.weight_inp, rowiloc,spanx+1, 1,spanx )
        rowiloc = 6
        lyt.addWidget( self.Gui.kern_x_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.kern_x_inp, rowiloc,spanx+1, 1,spanx )
        rowiloc = 7
        lyt.addWidget( self.Gui.kern_y_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.kern_y_inp, rowiloc,spanx+1, 1,spanx )
        rowiloc = 8
        lyt.addWidget( self.Gui.letter_spacing_lab, rowiloc,0, 1,spanx )
        lyt.addWidget( self.Gui.letter_spacing_inp, rowiloc,spanx+1, 1,spanx )
        
        lyt.setRowStretch( lyt.rowCount(), 1 )
        self.setLayout( lyt )
        
    def bt_save( self ):
        
        # parse gui
        screen_name = self.Gui.screen_name_line.text()
        derive_from = self.Gui.physical_types_cbx.currentText()
        scale = self.Gui.scale_inp.text()
        tilt = self.Gui.tilt_inp.text()
        weight = self.Gui.weight_inp.text()
        kern_x = self.Gui.kern_x_inp.text()
        kern_y = self.Gui.kern_y_inp.text()
        letter_spacing = self.Gui.letter_spacing_inp.text()
        
        # get unique name corresponding to this screen name
        unique_name = None
        for existing_unique_name, existing_screen_name in self.__cached_screen_names.items():
            if screen_name==existing_screen_name:
                unique_name = existing_unique_name
                break
        if unique_name is None:
            # this screen name is new, no existing
            # unique name corresponds to it
            unique_name = unique_loc()
        
        # save to disk
        self.Presets.LogicalType.new_preset(
            unique_name,
            screen_name,
            derive_from,
            scale,
            tilt,
            weight,
            kern_x,
            kern_y,
            letter_spacing
            )
        
    def bt_delete( self ):
        
        iloc = self.Gui.logical_types_cbx.currentIndex()
        
        unique_name = list( self.__cached_screen_names.keys() )[iloc]
        self.Presets.LogicalType.delete_preset( unique_name )
        
    def bt_clear( self ):
        
        self.Presets.LogicalType.clear_all_presets()
        
    def bt_load( self ):
        
        if len( self.__cached_screen_names ) == 0:
            return
        
        iloc = self.Gui.logical_types_cbx.currentIndex()
        
        unique_name = list( self.__cached_screen_names.keys() )[iloc]
        p = self.Presets.LogicalType.get_presets()[unique_name]
        
        c = self.Presets.LogicalType.Columns
        
        # fill gui
        self.Gui.screen_name_line.setText( p[c.SCREEN_NAME] )
        self.Gui.physical_types_cbx.setCurrentText( p[c.DERIVE_FROM] )
        self.Gui.scale_inp.setText( p[c.SCALE] )
        self.Gui.tilt_inp.setText( p[c.TILT] )
        self.Gui.weight_inp.setText( p[c.WEIGHT] )
        self.Gui.kern_x_inp.setText( p[c.KERN_X] )
        self.Gui.kern_y_inp.setText( p[c.KERN_Y] )
        self.Gui.letter_spacing_inp.setText( p[c.LETTER_SPACING] )
        
#---------------------------------------------------------------------------+++
# end 2023.05.14
# created
