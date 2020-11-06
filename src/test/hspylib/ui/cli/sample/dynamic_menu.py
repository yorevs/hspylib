from hspylib.ui.cli.factory.menu_factory import MenuFactory
from hspylib.ui.cli.menu_ui import MenuUi
from hspylib.ui.cli.menu_utils import MenuUtils

main_menu = sub_menu_1 = sub_menu_2 = None


def ret_main_menu(self):
    return main_menu


def ret_sub_menu_1(self):
    return sub_menu_1


def ret_sub_menu_2(self):
    return sub_menu_2


if __name__ == '__main__':
    main_menu = MenuFactory.INSTANCE \
        .create(None, 'Dynamic Main Menu') \
        .with_option('Exit').on_trigger(lambda t: MenuUtils.exit_app(0)) \
        .with_option('Sub-Menu-1').on_trigger(ret_sub_menu_1) \
        .with_option('Sub-Menu-2').on_trigger(ret_sub_menu_2) \
        .build()
    sub_menu_1 = MenuFactory.INSTANCE \
        .create(main_menu, 'Sub-Menu-1') \
        .with_option('Back').on_trigger(ret_main_menu) \
        .with_option('Print Hey').on_trigger(lambda t: print('Hey"')) \
        .with_option('Print Hoo').on_trigger(lambda t: print('Hoo"')) \
        .build()
    sub_menu_2 = MenuFactory.INSTANCE \
        .create(main_menu, 'Sub-Menu-2') \
        .with_option('Back').on_trigger(ret_main_menu) \
        .with_option('Print Hey').on_trigger(lambda t: print('Hello"')) \
        .with_option('Print Hoo').on_trigger(lambda t: print('Hi"')) \
        .build()
    mm = MenuUi(main_menu)
    mm.run()
