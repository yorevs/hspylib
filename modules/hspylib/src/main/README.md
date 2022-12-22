# HomeSetup Python Library - HSPyLib

## Your mature python application

[![License](https://badgen.net/badge/license/MIT/gray)](LICENSE.md)
[![Release](https://badgen.net/badge/release/v0.11.138/gray)](CHANGELOG.md#unreleased)
[![PyPi](https://badgen.net/badge/icon/python?icon=pypi&label)](https://pypi.org/project/hspylib)
[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/yorevs/hspylib)
[![Gitter](https://badgen.net/badge/icon/gitter?icon=gitter&label)](https://gitter.im/hspylib/community)
[![Donate](https://badgen.net/badge/paypal/donate/yellow)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=J5CDEFLF6M3H4)

HSPyLib is a Python library that will elevate your experience to another level. It relies on well known principles as
SOLID, DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid) and YAGNI (You Ain’t Gonna Need It). It provides many
frameworks and facilities to help you create mature python3 applications "PYCSNBASS" (Python Code Should Not Be A Simple
Script).

HSPyLib is a part of the [HomeSetup](https://github.com/yorevs/homesetup) project.

## Highlights

- Easy installation.
- Manager application that provides a helper to scaffold you applications.
- Widgets application that provides running built-in and custom widgets.
- Enhanced TUI helpers and input methods, to elevate you terminal UI applications.
- Crud framework to help with databases, repositories and services.
- HTTP Request helpers.
- Python3 application framework.
- HSPyLib widgets framework.
- Enable Properties and AppConfigs using various syntax's like .properties, .ini and .yaml.
- Well tested code and often pylint clean.
- Gradle build system with many extensions.

A menu select example:

```python
from hspylib.modules.cli.tui.extra.mselect import mselect

if __name__ == '__main__':
    it = [f"Item-{n}" for n in range(1, 21)]
    sel = mselect(it, max_rows=10)
    print(str(sel))
```

![MenuSelect](doc/images/screenshots/mselect.png "MenuSelect")

A menu choose example:

```python
from hspylib.modules.cli.tui.extra.mchoose import mchoose

if __name__ == '__main__':
    it = [f"Item-{n}" for n in range(1, 21)]
    sel = mchoose(it, max_rows=10)
    print(str(sel))
```

![MenuChoose](doc/images/screenshots/mchoose.png "MenuChoose")

A Dashboard example:

```python
from hspylib.modules.cli.icons.font_awesome.dashboard_icons import DashboardIcons
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.tui.extra.mdashboard.mdashboard import MenuDashBoard, mdashboard

if __name__ == '__main__':
  # fmt: off
  dashboard_items = MenuDashBoard.builder() \
      .item() \
          .icon(FormIcons.PLUS) \
          .tooltip('Add something') \
          .on_trigger(lambda: print('Add')) \
          .build() \
      .item() \
          .icon(FormIcons.MINUS) \
          .tooltip('Remove something') \
          .on_trigger(lambda: print('Del')) \
          .build() \
      .item() \
          .icon(FormIcons.EDIT) \
          .tooltip('Edit something') \
          .on_trigger(lambda: print('Edit')) \
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
  result = mdashboard(dashboard_items, 4)
```

![MenuDashboard](doc/images/screenshots/mdashboard.png "MenuDashboard")

A form input example

```python
from hspylib.modules.cli.tui.extra.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.extra.minput.minput import MenuInput, minput

if __name__ == '__main__':
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
            .min_max_length(1, 2) \
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
    print(result.__dict__)
```

![MenuInput](doc/images/screenshots/minput.png "MenuInput")

And many other cool features like repositories, Qt and CRUD helpers, etc...

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
- [4. Support HSPyLib](#support-hspylib)
- [5. Links](#links)

<!-- tocstop -->

## Installation

### Requirements

#### Operating Systems

- Darwin
  + High Sierra and higher
- Linux
  + Ubuntu 16 and higher
  + CentOS 7 and higher
  + Fedora 31 and higher

You may want to install HSPyLib on other OS's and it will probably work, but there are no guarantees that it
**WILL ACTUALLY WORK**.

#### Required software

The following software are required:

- Git (To clone the github repository)
- Gradle (To build the HSPyLib project)
- instantclient-basiclite-macos (To use oracle database repositories)

There are some python dependencies, but they will be automatically downloaded when the build runs.

### PyPi

To install HSPyLib from PyPi issue the command:

`# python3 -m pip install hspylib`

To upgrade HSPyLib use the command:

`# python3 -m pip install hspylib --upgrade`

### GitHub

To clone HSPyLib into your local machine issue the command:

`# git clone https://github.com/yorevs/hspylib.git`

## Documentation

TBD

## Contact

You can contact us using our [Gitter](https://gitter.im/hspylib/community) community or using our
[Reddit](https://www.reddit.com/user/yorevs).

## Support HSPyLib

You can support HSPyLib
by [donating](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=J5CDEFLF6M3H4)
or coding. Fell free to contact me for details. When contributing with code change please take a look at our
[guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=J5CDEFLF6M3H4)

## Links

- Documentation: TBD
- License: [MIT](LICENSE.md)
- Releases: https://pypi.org/project/hspylib/#history
- Code: https://github.com/yorevs/hspylib
- Issue tracker: https://github.com/yorevs/hspylib/issues
- Official chat: https://gitter.im/hspylib/community
- Contact: https://www.reddit.com/user/yorevs
- Mailto: yorevs@hotmail.com
