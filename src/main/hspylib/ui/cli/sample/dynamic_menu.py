from main.hspylib.ui.cli.menu_factory import MenuFactory
from main.hspylib.ui.cli.menu_ui import MenuUi
from main.hspylib.ui.cli.menu_utils import MenuUtils

main_menu = sub_menu_1 = sub_menu_2 = None


def ret_main_menu(self):
    return main_menu


def ret_sub_menu_1(self):
    return sub_menu_1


def ret_sub_menu_2(self):
    return sub_menu_2


if __name__ == '__main__':
    factory = MenuFactory.INSTANCE
    sub_menu_1 = factory\
        .create(None, 'Sub-Menu-1')\
            .with_option(0, 'Back')\
                .on_trigger(ret_main_menu)\
            .with_option(1, 'Print Hey')\
                .on_trigger(lambda t: print('Hey"'))\
            .with_option(2, 'Print Hoo')\
                .on_trigger(lambda t: print('Hoo"'))\
            .with_option(3, 'Lets go')\
                .on_trigger(lambda t: MenuUtils.exit_app(0))\
        .build()
    sub_menu_2 = factory\
        .create(None, 'Sub-Menu-2')\
            .with_option(0, 'Back')\
                .on_trigger(lambda t: print('-> Back'))\
            .with_option(1, 'Print Hey')\
                .on_trigger(lambda t: print('Hello"'))\
            .with_option(2, 'Print Hoo')\
                .on_trigger(lambda t: print('Hi"'))\
        .build()
    main_menu = factory\
        .create(None, 'Main Menu')\
            .with_option(0, 'Exit')\
                .on_trigger(lambda t: MenuUtils.exit_app(0))\
            .with_option(1, 'Sub-Menu-1')\
                .on_trigger(ret_sub_menu_1)\
            .with_option(2, 'Sub-Menu-2')\
                .on_trigger(ret_sub_menu_2)\
        .build()
    mm = MenuUi(main_menu)
    mm.run()
