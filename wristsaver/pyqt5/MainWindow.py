# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

log.setLevel( logging.DEBUG )

# embedded in python
import os
import sys
# pip install
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtGui import ( QIcon )
from PyQt5.QtWidgets import ( QWidget, QMainWindow,
    QMenu, QMainWindow, QGridLayout, QSplitter,
    QTabWidget, QPushButton )
# same project
from wristsaver import MainPaths
from wristsaver.writing_type.PhysicalTypeManager import PhysicalTypeManager
from wristsaver.common import ( readf, unique_loc )
from wristsaver.pyqt5.LogicalTypePresetsEditor import LogicalTypePresetsEditor
from wristsaver.pyqt5.PhysicalTypeEditor import PhysicalTypeEditor

class CentralWidget( QWidget ):
    
    # Orchestrates all the GUI work.
    
    class Folders:
        
        PHYSICAL_TYPES = PhysicalTypeManager.PREFERRED_SAVE_DIR_NAME
        
    class Doers:
        
        PhysicalTypeManager = None
    
    class Gui:
        
        disposable_widgets = None
        
        tab_widget = None
        side_pane = None
        
        split_hmid = None

    __pending_physical_type_reload = False

    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( CentralWidget, self ).__init__( parent, *args, **kwargs )
        
        # paths
        self.Folders.PHYSICAL_TYPES = MainPaths.set_folder( self.Folders.PHYSICAL_TYPES )
        
        # doers
        self.Doers.PhysicalTypeManager = PhysicalTypeManager( self.Folders.PHYSICAL_TYPES )
        
        # gui
        
        self.Gui.disposable_widgets = []
        
        # left pane
        
        side_widget1 = QWidget( parent=self )
        side_lyt1 = QGridLayout()
        #side_lyt1.setSpacing(0)
        #side_lyt1.setAlignment( Qt.AlignTop&Qt.AlignLeft )
        bt_physical_type_folder = QPushButton( 'Open Physical Type Folder', parent=self )
        bt_physical_type_folder.clicked.connect( self.__open_physical_type_folder_event )
        bt_physical_type_folder.setToolTip( 'Manually create new/delete/duplicate folders' )
        bt_logical_type_presets_editor = QPushButton( 'Logical Type Presets Editor', parent=self )
        bt_logical_type_presets_editor.clicked.connect( self.__new_logical_type_presets_editor )
        bt_oto_ini_editor = QPushButton( 'Physical Type Editor', parent=self )
        bt_oto_ini_editor.clicked.connect( self.__new_physical_type_editor_event )
        side_lyt1.addWidget( bt_physical_type_folder, 0,0 )
        side_lyt1.addWidget( bt_oto_ini_editor, 1,0 )
        side_lyt1.addWidget( bt_logical_type_presets_editor, 2,0 )
        side_lyt1.setRowStretch( side_lyt1.rowCount(), 1 )
        side_lyt1.setColumnStretch( side_lyt1.columnCount(), 1 )
        side_widget1.setLayout( side_lyt1 )
        
        side_widget2 = QWidget( parent=self )
        side_lyt2 = QGridLayout()
        side_lyt2.setSpacing(0)
        #side_lyt2.setAlignment( Qt.AlignTop&Qt.AlignLeft )
        side_lyt2.setRowStretch( side_lyt2.rowCount(), 1 )
        side_lyt2.setColumnStretch( side_lyt2.columnCount(), 1 )
        side_widget2.setLayout( side_lyt2 )
        
        self.Gui.side_pane = QTabWidget( parent=self )
        self.Gui.side_pane.setContentsMargins(0,0,0,0)
        self.Gui.side_pane.addTab( side_widget1, 'Actions' )
        self.Gui.side_pane.addTab( side_widget2, '⚙️' )
        
        # main area
        
        self.Gui.tab_widget = QTabWidget( parent=self )
        self.Gui.tab_widget.setContentsMargins(0,0,0,0)
        self.Gui.tab_widget.setTabsClosable(True)
        self.Gui.tab_widget.tabCloseRequested.connect( self.__close_main_area_tab_event )
        
        # assemble
        
        lyt = QGridLayout()
        #lyt.setSpacing(0)
        #lyt.setAlignment( Qt.AlignTop&Qt.AlignLeft )
        
        self.Gui.split_hmid = QSplitter( Qt.Horizontal, parent=self )
        self.Gui.split_hmid.addWidget( self.Gui.side_pane )
        self.Gui.split_hmid.addWidget( self.Gui.tab_widget )
        self.Gui.split_hmid.setStretchFactor( 0,1 )
        self.Gui.split_hmid.setStretchFactor( 1,250 ) # how does this stupid thing work
        
        lyt.addWidget( self.Gui.split_hmid, 0,0 )
        
        self.setLayout( lyt )
        
    def __close_main_area_tab_event( self, tabiloc ):
        
        # help:
        # https://stackoverflow.com/questions/61342380/pyqt5-closeable-tabs-in-qtabwidget
        
        w = self.Gui.tab_widget.widget( tabiloc )
        w.deleteLater()
        del w
        
        self.Gui.tab_widget.removeTab( tabiloc )
        
    def satisfy_pending_reloads( self ):
        
        # It is easier to do allow user to manually
        # manage some folders and reload their contents on demand
        # rather then implement unstable
        # new/rename/delete/duplicate functionality.
        # Also, that's how UTAU allows user to manage voicebanks.
        
        if self.__pending_physical_type_reload:
            
            # already existing comboboxes will not be affected
            # TODO
            # implement custom combobox that reads items
            # directly from PhysicalTypeManager reference,
            # rather then creates a copy
            self.Doers.PhysicalTypeManager._load()
            self.__pending_physical_type_reload = False
        
    def __open_physical_type_folder_event( self ):
        
        self.__pending_physical_type_reload = True
        
        src = self.Doers.PhysicalTypeManager.get_save_folder()
        os.startfile( src )
        
    def __new_physical_type_editor_event( self ):
        
        w = PhysicalTypeEditor( self.Doers.PhysicalTypeManager )
        self.Gui.disposable_widgets.append( w )
        
        self.Gui.tab_widget.addTab( w, 'Physical' )
        
    def __new_logical_type_presets_editor( self ):
        
        w = LogicalTypePresetsEditor( self.Doers.PhysicalTypeManager )
        self.Gui.disposable_widgets.append( w )
        
        self.Gui.tab_widget.addTab( w, 'Logical' )

class MainWindow( QMainWindow ):
    
    # It does nothing.

    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( MainWindow, self ).__init__( parent, *args, **kwargs )
        
        cw = CentralWidget( parent=self )
        self.setCentralWidget( cw )
        
        self.setWindowTitle( 'Main Window — wristsaver' )
        
    def changeEvent( self, ev ):
        
        # help:
        # https://stackoverflow.com/questions/16721557/how-to-detect-if-a-window-has-been-activated
        
        print( ev.type(), ev.type()==QEvent.ActivationChange )
        
        if ev.type()==QEvent.ActivationChange:
        
            if self.isActiveWindow():
                self.centralWidget().satisfy_pending_reloads()
        
#---------------------------------------------------------------------------+++
# end 2023.05.16
# added another button
