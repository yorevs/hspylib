#!/usr/bin/env python3
from hspylib.ui.cli.icons.font_awesome.ui_compose.form_icons import FormIcons
from hspylib.ui.cli.menu.extra.mdashboard import MenuDashBoard, mdashboard

if __name__ == '__main__':
    # @formatter:off
    dashboard_items = MenuDashBoard.builder() \
        .item() \
            .icon(FormIcons.ON) \
            .tooltip('Add something') \
            .action(lambda: print('Add')) \
            .build() \
        .item() \
            .icon(FormIcons.OFF) \
            .tooltip('Remove something') \
            .action(lambda: print('Del')) \
            .build() \
        .item() \
            .icon(FormIcons.EDITABLE) \
            .tooltip('Edit something') \
            .action(lambda: print('Edit')) \
            .build() \
        .item() \
            .icon(FormIcons.UNCHECK_CIRCLE) \
            .tooltip('List everything') \
            .action(lambda: print('List')) \
            .build() \
        .item() \
            .icon(FormIcons.VISIBLE) \
            .tooltip('Show everything') \
            .action(lambda: print('Show')) \
            .build() \
        .item() \
            .icon(FormIcons.EXIT) \
            .tooltip('Exit application') \
            .action(lambda: print('Exit')) \
            .build() \
        .build()
    # @formatter:on
    result = mdashboard(dashboard_items, 3)
