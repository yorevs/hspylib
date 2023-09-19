# <img src="https://iili.io/HYBJFA7.png"  width="34" height="34"> HomeSetup Python Library - HsPyLib

## Your Python code is not JUST a script !!

[![License](https://badgen.net/badge/license/MIT/gray)](LICENSE.md)
[![Release](https://badgen.net/badge/release/v0.9.9/gray)](docs/CHANGELOG.md#unreleased)
[![PyPi](https://badgen.net/badge/icon/python?icon=pypi&label)](https://pypi.org/project/hspylib)
[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/yorevs/hspylib)
[![Gitter](https://badgen.net/badge/icon/gitter?icon=gitter&label)](https://gitter.im/hspylib/community)
[![Donate](https://badgen.net/badge/paypal/donate/yellow)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=J5CDEFLF6M3H4)

HsPyLib is a Python library that will elevate your experience to another level. It relies on well known principles as
SOLID, DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid) and YAGNI (You Ain’t Gonna Need It). It provides many
frameworks and facilities to help you create mature python3 applications "PYCSNBASS" (Python Code Should Not Be A Simple
Script).

HsPyLib is a part of the [HomeSetup](https://github.com/yorevs/homesetup) project.

## Highlights

- Easy installation.
- Application manager that provides a helper to scaffold your python applications.
- Widgets manager that provides running 'built-in' and custom python widgets.
- Enhanced TUI helpers and input methods, to elevate your UXP with terminal applications.
- crud framework to help with databases, repositories and services.
- HTTP request helpers.
- Enable Properties and AppConfigs using the most common extensions such as .properties, toml, yml...
- Well tested code and often pylint clean.
- Gradle build system with many extensions.
- Various demos to help understand the library.

- [A Kafka manager](modules/kafman/src/main/README.md) application tool.
- [A Cloud Foundry](modules/cfman/src/main/README.md) application tool.
- [A Firebase](modules/firebase/src/main/README.md) application tool.
- [A Vault provider](modules/vault/src/main/README.md) tool.
- [A CLI Terminal](modules/clitt/src/main/README.md) framework.
- [A PyQt](modules/hqt/src/main/README.md) applications framework.

Create an easy to use and code multiple select or choose input method:

```python
from hspylib.modules.cli.vt100.vt_color import VtColor

from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.tui.mselect.mselect import mselect
from clitt.core.tui.tui_preferences import TUIPreferences


class SelectableItem:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Name: {self.name} Value: {self.value}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    TUIPreferences(
        max_rows=10,
        highlight_color=VtColor.WHITE,
        selected=NavIcons.SELECTED,
        unselected=NavIcons.UNSELECTED,
    )
    quantity = 22
    digits = len(str(quantity))
    it = [SelectableItem(f"Item-{n:>0{digits}}", f"Value-{n:>0{digits}}") for n in range(1, quantity)]
    sel = mselect(it)
    print(str(sel))
```

![MenuSelect](https://iili.io/HYBFh74.png "MenuSelect")

```python
from hspylib.modules.cli.vt100.vt_color import VtColor

from clitt.core.tui.mchoose.mchoose import mchoose
from clitt.core.tui.tui_preferences import TUIPreferences


class ChooseableItem:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Name: {self.name} Value: {self.value}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    TUIPreferences(
        max_rows=10, highlight_color=VtColor.WHITE
    )
    quantity = 22
    digits = len(str(quantity))
    it = [ChooseableItem(f"Item-{n:>0{digits}}", f"Value-{n:>0{digits}}") for n in range(1, quantity)]
    sel = mchoose(it)
    print(str(sel))
```

![MenuChoose](https://iili.io/HYBFwp2.png "MenuChoose")

Create beautiful form inputs:

```python
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.minput import MenuInput, minput

if __name__ == "__main__":
    # fmt: off
    form_fields = MenuInput.builder() \
        .field() \
            .label('letters') \
            .validator(InputValidator.letters()) \
            .build() \
        .field() \
            .label('word') \
            .validator(InputValidator.words()) \
            .build() \
        .field() \
            .label('number') \
            .validator(InputValidator.numbers()) \
            .min_max_length(1, 4) \
            .build() \
        .field() \
            .label('masked') \
            .itype('masked') \
            .value('|##::##::## @@') \
            .build() \
        .field() \
            .label('selectable') \
            .itype('select') \
            .value('one|two|three') \
            .build() \
        .field() \
            .label('checkbox') \
            .itype('checkbox') \
            .build() \
        .field() \
            .label('password') \
            .itype('password') \
            .validator(InputValidator.anything()) \
            .min_max_length(4, 8) \
            .build() \
        .field() \
            .label('read-only') \
            .access_type('read-only') \
            .value('READ-ONLY') \
            .build() \
        .build()
    # fmt: on

    result = minput(form_fields)
    print(result.__dict__ if result else "None")
```

![MenuInput](https://iili.io/HYBFVrG.png "MenuInput")

Or even create nice dashboards:

```python
from hspylib.modules.cli.vt100.vt_color import VtColor

from clitt.core.icons.font_awesome.dashboard_icons import DashboardIcons
from clitt.core.tui.mdashboard.mdashboard import mdashboard, MenuDashBoard
from clitt.core.tui.tui_preferences import TUIPreferences

if __name__ == "__main__":
    TUIPreferences(
        max_rows=10,
        items_per_line=3,
        highlight_color=VtColor.WHITE
    )
    # fmt: off
    dashboard_items = MenuDashBoard.builder() \
        .item() \
            .icon(DashboardIcons.POWER) \
            .tooltip('Do something') \
            .on_trigger(lambda: print('Something')) \
            .build() \
        .item() \
            .icon(DashboardIcons.MOVIE) \
            .tooltip('Another something') \
            .on_trigger(lambda: print('Another')) \
            .build() \
        .item() \
            .icon(DashboardIcons.NOTIFICATION) \
            .tooltip('Notify something') \
            .on_trigger(lambda: print('Notification')) \
            .build() \
        .item() \
            .icon(DashboardIcons.LIST) \
            .tooltip('List everything') \
            .on_trigger(lambda: print('List')) \
            .build() \
        .item() \
            .icon(DashboardIcons.DATABASE) \
            .tooltip('Database console') \
            .on_trigger(lambda: print('Database')) \
            .build() \
        .item() \
            .icon(DashboardIcons.EXIT) \
            .tooltip('Exit application') \
            .on_trigger(lambda: print('Exit')) \
            .build() \
        .build()
    # fmt: on

    result = mdashboard(dashboard_items)
```

![MenuDashboard](https://iili.io/HYBFX2f.png "MenuDashboard")

## Table of contents

<!-- toc -->

- [1. Installation](#installation)
  * [1.1. Requirements](#requirements)
    + [1.1.1. Operating systems](#operating-systems)
    + [1.1.2. Required software](#required-software)
  * [1.2. PyPi](#pypi)
  * [1.3. GitHub](#github)
- [2. Documentation](#documentation)
- [3. Contact](#contact)
- [4. Support HsPyLib](#support-hspylib)
- [5. Links](#links)

<!-- tocstop -->

## Installation

### Requirements

#### Python

- Python 3.10 and higher

#### Operating Systems

- Darwin
  + High Sierra and higher
- Linux
  + Ubuntu 16 and higher
  + CentOS 7 and higher
  + Fedora 31 and higher

You may want to install HsPyLib on other OS's and it will probably work, but there are no guarantees that it
**WILL ACTUALLY WORK**.

#### Required software

The following software are required:

- Git (To clone the github repository)
- Gradle (To build the HsPyLib project)

There are some python dependencies, but they will be automatically downloaded when the build runs.

### PyPi

To install HsPyLib from PyPi issue the command:

`# python3 -m pip install hspylib`

To upgrade HsPyLib use the command:

`# python3 -m pip install hspylib --upgrade`

Additional modules that can also be installed:

- [CLItt](https://pypi.org/project/hspylib-clitt) : `# python3 -m pip install hspylib-clitt` to install HsPyLib CLI terminal tools.
- [Firebase](https://pypi.org/project/hspylib-firebase) : `# python3 -m pip install hspylib-firebase` to install HsPyLib Firebase application.
- [Vault](https://pypi.org/project/hspylib-vault) : `# python3 -m pip install hspylib-vault` to install HsPyLib Vault application.
- [CFMan](https://pypi.org/project/hspylib-cfman) : `# python3 -m pip install hspylib-cfman` to install CloudFoundry manager.
- [Kafman](https://pypi.org/project/hspylib-kafman) : `# python3 -m pip install hspylib-kafman` to install Kafka manager.
- [Datasource](https://pypi.org/project/hspylib-datasource) : `# python3 -m pip install hspylib-datasource` to install datasource helpers.
- [HQT](https://pypi.org/project/hspylib-hqt) : `# python3 -m pip install hspylib-hqt` to install HsPyLib PyQt framework.

### GitHub

To clone HsPyLib into your local machine type the command:

`# git clone https://github.com/yorevs/hspylib.git`

## Documentation

The API documentation can be found [here](docs/api/index.html)

## Contact

You can contact us using our [Gitter](https://gitter.im/hspylib/community) community or using our
[Reddit](https://www.reddit.com/user/yorevs).

## Support HsPyLib

You can support HsPyLib
by [donating](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=J5CDEFLF6M3H4)
or coding. Fell free to contact me for details. When contributing with code change please take a look at our
[guidelines](docs/CONTRIBUTING.md) and [code of conduct](docs/CODE_OF_CONDUCT.md).

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=J5CDEFLF6M3H4)

## Sponsors

This project is supported by:

<a href="https://www.jetbrains.com/community/opensource/?utm_campaign=opensource&utm_content=approved&utm_medium=email&utm_source=newsletter&utm_term=jblogo#support">
  <img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png" width="120" height="120">
</a>

Thank you for your support <3 !!

## Links

- Documentation: [API](docs/api/index.html)
- License: [MIT](LICENSE.md)
- Releases: https://pypi.org/project/hspylib/#history
- Code: https://github.com/yorevs/hspylib
- Issue tracker: https://github.com/yorevs/hspylib/issues
- Official chat: https://gitter.im/hspylib/community
- Contact: https://www.reddit.com/user/yorevs
- Mailto: [Yorevs](mailto:yorevs@hotmail.com)
