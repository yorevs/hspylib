#!/usr/bin/env python3
from hspylib.ui.cli.factory.menu_factory import MenuFactory
from hspylib.ui.cli.menu.menu_ui import MenuUi
from hspylib.ui.cli.menu.menu_utils import MenuUtils


if __name__ == '__main__':
    main_menu = MenuFactory().INSTANCE \
        .create(None, 'Dynamic Main Menu') \
        .with_option('Exit').on_trigger(lambda t: MenuUtils.exit_app(0)) \
        .with_option('Sub-Menu-1').on_trigger(lambda x: sub_menu_1) \
        .with_option('Sub-Menu-2').on_trigger(lambda x: sub_menu_2) \
        .build()
    sub_menu_1 = MenuFactory().INSTANCE \
        .create(main_menu, 'Sub-Menu-1') \
        .with_option('Back').on_trigger(lambda x: main_menu) \
        .with_option('Print Hey').on_trigger(lambda t: print('Hey')) \
        .with_option('Print Hoo').on_trigger(lambda t: print('Hoo')) \
        .build()
    sub_menu_2 = MenuFactory().INSTANCE \
        .create(main_menu, 'Sub-Menu-2') \
        .with_option('Back').on_trigger(lambda x: main_menu) \
        .with_option('Print Hello').on_trigger(lambda t: print('Hello')) \
        .with_option('Print Hi').on_trigger(lambda t: print('Hi')) \
        .build()
    mm = MenuUi(main_menu)
    mm.run()
