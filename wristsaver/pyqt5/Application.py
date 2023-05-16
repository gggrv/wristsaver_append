# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

log.setLevel( logging.DEBUG )

# embedded in python
# pip install
from PyQt5.QtCore import ( QCoreApplication )
from PyQt5.QtWidgets import ( QApplication )
# same project
from wristsaver.pyqt5.MainWindow import MainWindow
    
class Application( QApplication ):
    
    main_window = None
    
    def __init__( self,
                  sys_argv,
                  *args, **kwargs ):
        super( Application, self ).__init__( sys_argv, *args, **kwargs )

        self.main_window = MainWindow()
        self.main_window.show()
        
        # gui mainloop
        self.exec_()
        self.exit_mainloop()

    def exit_mainloop( self ):
        log.debug( 'exited mainloop, now exiting app' )
        QCoreApplication.exit()

#---------------------------------------------------------------------------+++
# end 2023.05.14
# appropriated from another project
