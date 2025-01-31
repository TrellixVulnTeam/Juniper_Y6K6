"""
Host application specific menu object.
- For applications which use Qt this will wrap QMenu
- For other programs which we are able to wrap, this will wrap the program specific object
- For programs which have no exposure, this will be empty / logicless
"""
from qtpy import QtWidgets

import juniper
import juniper.decorators


class QMenuWrapper(object):
    def __init__(self, name, display_name):
        """
        Top level menu object wrapper
        :param <str:name> Code name of the menu
        :param <str:display_name> Friendly / display name of the menu
        :return <object:menu> Menu object, type can change depending on the host application
        """
        self.menu_object = None
        self.name = name
        self.display_name = display_name
        self.__initialize_menu()

    @juniper.decorators.virtual_method
    def __initialize_menu(self):
        raise NotImplementedError

    @__initialize_menu.override("juniper_hub")
    def _initialize_menu(self):
        import juniper_hub.juniper_hub
        menu = juniper_hub.juniper_hub.JuniperHub().menu
        self.menu_object = menu
        return menu

    @__initialize_menu.override("painter")
    def _initialize_menu(self):
        import substance_painter.ui
        menu = QtWidgets.QMenu(self.display_name, None)
        menu.setToolTipsVisible(True)
        menu.setObjectName(self.display_name)
        substance_painter.ui.add_menu(menu)
        self.menu_object = menu

    @__initialize_menu.override("designer")
    def _initialize_menu(self):
        import sd
        uimgr = sd.getContext().getSDApplication().getQtForPythonUIMgr()
        menu = QtWidgets.QMenu(self.name, None)
        menu.setToolTipsVisible(True)
        menu.setObjectName(self.display_name)
        uimgr.newMenu(self.display_name, self.name)
        self.menu_object = uimgr.findMenuFromObjectName(self.name)

    @__initialize_menu.override("unreal")
    def _initialize_menu(self):
        import unreal
        menus = unreal.ToolMenus.get()
        main_menu = menus.find_menu("LevelEditor.MainMenu")
        juniper_menu = main_menu.add_sub_menu(main_menu.get_name(), self.display_name, self.display_name, self.display_name)
        juniper_menu.searchable = True
        menus.refresh_all_widgets()
        self.menu_object = juniper_menu

    @__initialize_menu.override("max")
    def _initialize_menu(self):
        import qtmax
        toolbar = qtmax.GetQMaxMainWindow()

        for i in list(toolbar.menuBar().actions()):
            if(i.text() == "Juniper"):
                toolbar.menuBar().removeAction(i)

        main_menu = QtWidgets.QMenu(self.display_name, toolbar)
        main_menu.setToolTipsVisible(True)
        main_menu.setObjectName(self.name)
        toolbar.menuBar().addMenu(main_menu)
        self.menu_object = main_menu

    @__initialize_menu.override("blender")
    def _initialize_menu(self):
        import bpy

        class blender_menu(bpy.types.Menu):
            bl_label = "Juniper"
            bl_idname = "jinterface.menu"

            def draw(self_, context):
                layout = self_.layout
                layout.operator("object.select_all", text="Select").action = "TOGGLE"

        def draw_item(self_, context):
            self_.layout
            self_.layout.menu(blender_menu.bl_idname)

        bpy.utils.register_class(blender_menu)
        bpy.types.TOPBAR_MT_editor_menus.append(draw_item)
        self.menu_object = blender_menu

    # ----------------------------------------------------------------

    @juniper.decorators.virtual_method
    def add_separator(self):
        """
        Add a separator to the menu
        """
        if(self.menu_object):
            self.menu_object.addSeparator()

    @add_separator.override("unreal")
    def _add_separator(self):
        import unreal
        action = unreal.ToolMenuEntry(
            type=unreal.MultiBlockType.SEPARATOR,
            insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT))
        self.menu_object.add_menu_entry("Juniper", action)

    @add_separator.override("blender")
    def _add_separator(self):
        # TODO! ToolsMenu: Blender: Implement separators for blender
        pass
