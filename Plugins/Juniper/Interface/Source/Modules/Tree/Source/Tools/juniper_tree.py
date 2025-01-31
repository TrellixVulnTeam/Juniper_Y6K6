"""
:type tool
:category Project Tools
:summary Launches the Juniper Tree as a standalone app
:icon icons\\standard\\app_default.png
"""
import jinterface.tree
import juniper.widgets as qt_utils

import juniper


app = qt_utils.get_application()
jinterface.tree.JuniperTreeManager().create_tree(force=True)

if(juniper.program_context in ("python",)):
    app.exec_()
