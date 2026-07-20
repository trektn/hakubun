# This file is part of Trackma.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from hakubun.ui.qt.widgets import DetailsWidget


class DetailsDialog(QDialog):
    def __init__(self, parent, worker, show, on_go_to=None):
        QDialog.__init__(self, parent)
        self.setMinimumSize(530, 550)
        self.setWindowTitle('Details')
        self.worker = worker
        self.on_go_to = on_go_to

        main_layout = QVBoxLayout()
        details = DetailsWidget(self, worker)
        main_layout.addWidget(details)

        bottom_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        bottom_buttons.setCenterButtons(True)
        bottom_buttons.rejected.connect(self.close)

        # Only set when this show is already in the user's list (see
        # AddDialog.s_show_details) -- lets the user jump straight to it
        # in the main list instead of going through Add again.
        if on_go_to is not None:
            go_to_btn = bottom_buttons.addButton(
                'Go to', QDialogButtonBox.ButtonRole.ActionRole)
            go_to_btn.clicked.connect(self.s_go_to)

        main_layout.addWidget(bottom_buttons)

        self.setLayout(main_layout)
        details.load(show)

    def s_go_to(self):
        self.on_go_to()
        self.close()
