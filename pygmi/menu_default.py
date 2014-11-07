# -----------------------------------------------------------------------------
# Name:        menu_default.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2013 Council for Geoscience
# Licence:     GPL-3.0
#
# This file is part of PyGMI
#
# PyGMI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGMI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
""" File Menu Routines """

# pylint: disable=E1101, C0103
from PyQt4 import QtGui, QtCore
import webbrowser


class FileMenu(object):
    """ Widget class to call the main interface """
    def __init__(self, parent):

        self.parent = parent
        context_menu = self.parent.context_menu

# File Menu

        self.menufile = QtGui.QMenu(parent.menubar)
        self.menufile.setTitle("File")
        parent.menubar.addAction(self.menufile.menuAction())

        self.action_open_project = QtGui.QAction(parent)
        self.action_open_project.setText("Open Project")
#        self.menufile.addAction(self.action_open_project)

        self.action_save_project = QtGui.QAction(parent)
        self.action_save_project.setText("Save Project")
#        self.menufile.addAction(self.action_save_project)

        self.action_exit = QtGui.QAction(parent)
#        self.menufile.addSeparator()
        self.action_exit.setText("Exit")
        self.menufile.addAction(self.action_exit)

        QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL("triggered()"),
                               parent.close)

# Context menus
        context_menu['Basic'].addSeparator()

        self.action_bandselect = QtGui.QAction(self.parent)
        self.action_bandselect.setText("Select Bands")
        context_menu['Basic'].addAction(self.action_bandselect)
        self.action_bandselect.triggered.connect(self.bandselect)

    def bandselect(self):
        """ Select bands """
        self.parent.launch_context_item_indata(ComboBoxBasic)


class ComboBoxBasic(QtGui.QDialog):
    """
    A basic combo box application
    """

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.parent = parent
        self.indata = {}
        self.outdata = {}

        # create GUI
        self.setWindowTitle('Band Selection')

        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        self.combo = QtGui.QListWidget()
        self.combo.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.vbox.addWidget(self.combo)

        self.buttonbox = QtGui.QDialogButtonBox()
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setCenterButtons(True)
        self.buttonbox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.vbox.addWidget(self.buttonbox)

        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

    def run(self):
        """ runs class """
        self.parent.scene.selectedItems()[0].update_indata()
        my_class = self.parent.scene.selectedItems()[0].my_class

        data = my_class.indata.copy()

        for j in data.keys():
            if j is 'Model3D' or j is 'Seis':
                continue

            tmp = []
            for i in data[j]:
                tmp.append(i.dataid)
            self.combo.addItems(tmp)

        if len(tmp) == 0:
            return

        tmp = self.exec_()

        if tmp != 1:
            return

        for j in data.keys():
            if j is 'Model3D' or j is 'Seis':
                continue
            atmp = [i.text() for i in self.combo.selectedItems()]

            if len(atmp) > 0:
                dtmp = []
                for i in data[j]:
                    if i.dataid in atmp:
                        dtmp.append(i)
                data[j] = dtmp

        my_class.indata = data

        if hasattr(my_class, 'data_init'):
            my_class.data_init()

        return True


class HelpMenu(object):
    """ Widget class to call the main interface """
    def __init__(self, parent):

        self.parent = parent

# Help Menu

        self.menuhelp = QtGui.QMenu(parent.menubar)
        parent.menubar.addAction(self.menuhelp.menuAction())

        self.action_help = QtGui.QAction(self.parent)
        self.action_about = QtGui.QAction(self.parent)

        self.menuhelp.addAction(self.action_help)
        self.menuhelp.addAction(self.action_about)

        self.menuhelp.setTitle("Help")
        self.action_help.setText("Help")
        self.action_about.setText("About")

        self.action_about.triggered.connect(self.about)
        self.action_help.triggered.connect(self.help)

    def about(self):
        """ PyGMI About Box """

        msg = '''\
Name:         PyGMI - Python Geophysical Modelling and Interpretation
Author:       Patrick Cole
E-Mail:       pcole@geoscience.org.za

Copyright:    (c) 2013 Council for Geoscience
Licence:      GPL-3.0

PyGMI is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

PyGMI is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see http://www.gnu.org/licenses/'''

        QtGui.QMessageBox.about(self.parent, 'PyGMI', msg)

    def help(self):
        """ Help File"""
        webbrowser.open(r'http://patrick-cole.github.io/pygmi/')
