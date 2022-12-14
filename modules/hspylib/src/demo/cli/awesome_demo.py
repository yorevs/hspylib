from hspylib.modules.cli.icons.font_awesome.app_icons import AppIcons
from hspylib.modules.cli.icons.font_awesome.awesome import demo_unicodes, demo_icons
from hspylib.modules.cli.icons.font_awesome.dashboard_icons import DashboardIcons
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons

if __name__ == '__main__':
    print('\nAppIcons ' + '-' * 30)
    demo_icons(awesome=AppIcons, split_columns=10)

    print('\n\nDashboardIcons ' + '-' * 30)
    demo_icons(awesome=DashboardIcons, split_columns=10)

    print('\n\nFormIcons ' + '-' * 30)
    demo_icons(awesome=FormIcons, split_columns=10)

    print('\n\nNavIcons ' + '-' * 30)
    demo_icons(awesome=NavIcons, split_columns=10)

    print('\n\nWidgetIcons ' + '-' * 30)
    demo_icons(awesome=WidgetIcons, split_columns=10)

    # print('\n\nALL UNICODES ' + '-' * 30)
    # demo_unicodes()
