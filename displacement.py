# -*- coding: utf-8 -*-

#******************************************************************************
#
# GenPoints
# ---------------------------------------------------------
# Generate regular points inside polygon
#
# Copyright (C) 2011 Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from __init__ import mVersion

import displacementdialog

import resources

class DisplacementPlugin( object ):
  def __init__( self, iface ):
    self.iface = iface
    self.iface = iface
    try:
      self.QgisVersion = unicode( QGis.QGIS_VERSION_INT )
    except:
      self.QgisVersion = unicode( QGis.qgisVersion )[ 0 ]

    # For i18n support
    userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/displacement"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/displacement"

    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

    if QFileInfo( userPluginPath ).exists():
      translationPath = userPluginPath + "/i18n/displacement_" + localeFullName + ".qm"
    else:
      translationPath = systemPluginPath + "/i18n/displacement_" + localeFullName + ".qm"

    self.localePath = translationPath
    if QFileInfo( self.localePath ).exists():
      self.translator = QTranslator()
      self.translator.load( self.localePath )
      QCoreApplication.installTranslator( self.translator )

  def initGui( self ):
    if int( self.QgisVersion ) < 1:
      QMessageBox.warning( self.iface.mainWindow(), "Point displacement",
                           QCoreApplication.translate( "Point displacement", "Quantum GIS version detected: " ) + unicode( self.QgisVersion ) + ".xx\n" +
                           QCoreApplication.translate( "Point displacement", "This version of Point displacement requires at least QGIS version 1.0.0\nPlugin will not be enabled." ) )
      return None

    self.actionRun = QAction( QIcon( ":/displacement.png" ), "Point displacement", self.iface.mainWindow() )
    self.actionRun.setStatusTip( QCoreApplication.translate( "Point displacement", "Generate regular points inside polygon" ) )
    self.actionAbout = QAction( QIcon( ":/about.png" ), "About", self.iface.mainWindow() )

    QObject.connect( self.actionRun, SIGNAL( "triggered()" ), self.run )
    QObject.connect( self.actionAbout, SIGNAL( "triggered()" ), self.about )

    if hasattr( self.iface, "addPluginToVectorMenu" ):
      self.iface.addPluginToVectorMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionRun )
      self.iface.addPluginToVectorMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionAbout )
      self.iface.addVectorToolBarIcon( self.actionRun )
    else:
      self.iface.addPluginToMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionRun )
      self.iface.addPluginToMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionAbout )
      self.iface.addToolBarIcon( self.actionRun )

  def unload( self ):
    if hasattr( self.iface, "addPluginToVectorMenu" ):
      self.iface.removePluginVectorMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionRun )
      self.iface.removePluginVectorMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionAbout )
      self.iface.removeVectorToolBarIcon( self.actionRun )
    else:
      self.iface.removePluginMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionRun )
      self.iface.removePluginMenu( QCoreApplication.translate( "Point displacement", "Point displacement" ), self.actionAbout )
      self.iface.removeToolBarIcon( self.actionRun )      

  def about( self ):
    dlgAbout = QDialog()
    dlgAbout.setWindowTitle( QApplication.translate( "Point displacement", "About Point displacement", "Window title" ) )
    lines = QVBoxLayout( dlgAbout )
    title = QLabel( QApplication.translate( "Point displacement", "<b>GenPoints</b>" ) )
    title.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
    lines.addWidget( title )
    version = QLabel( QApplication.translate( "Point displacement", "Version: %1" ).arg( mVersion ) )
    version.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
    lines.addWidget( version )
    lines.addWidget( QLabel( QApplication.translate( "Point displacement", "Generate regular points inside polygon" ) ) )
    lines.addWidget( QLabel( QApplication.translate( "Point displacement", "<b>Developers:</b>" ) ) )
    lines.addWidget( QLabel( "  Alexander Bruy" ) )
    lines.addWidget( QLabel( QApplication.translate( "Point displacement", "<b>Homepage:</b>") ) )

    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

    localeShortName = localeFullName[ 0:2 ]
    if localeShortName in [ "ru", "uk" ]:
      link = QLabel( "<a href=\"http://gis-lab.info/qa/genpoints.html\">http://gis-lab.info/qa/genpoints.html</a>" )
    else:
      link = QLabel( "<a href=\"http://gis-lab.info/qa/genpoints-eng.html\">http://gis-lab.info/qa/genpoints-eng.html</a>" )

    link.setOpenExternalLinks( True )
    lines.addWidget( link )

    btnClose = QPushButton( QApplication.translate( "Point displacement", "Close" ) )
    lines.addWidget( btnClose )
    QObject.connect( btnClose, SIGNAL( "clicked()" ), dlgAbout, SLOT( "close()" ) )

    dlgAbout.exec_()

  def run( self ):
    dlg = displacementdialog.DisplacementDialog( self.iface )
    dlg.exec_()