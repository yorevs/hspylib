# HSPyLib TODOs

## HSPYLIB

1. Check if execute SQLs, use params instead of values inside sql string.
2. Add a repository for SQLite db + tests.
3. Add a repository for Postgres db + tests.
4. Include a form validator for minput.
5. Improve tui -> extra with settings and remove parameters.
6. Update all README.md.
7. Fix pypi deployment:
   1. https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
   2. https://packaging.python.org/en/latest/tutorials/packaging-projects/
8. Use virtual environments: https://www.geeksforgeeks.org/python-virtual-environment/
9. Fix appman after gradle changes.

## HSPYLIB-VAULT

1. Add vault TUI

## HSPYLIB-KAFMAN

1. Install Droid font with kafman pip install
    '''int id = QFontDatabase::addApplicationFont(":/SMSicons/segoeui_0.ttf");
    QString family = QFontDatabase::applicationFontFamilies(id).at(0);
    QFont _font(family, 8);
    qApp->setFont(_font);'''
2. Implement json schema type form builder
   2.1. Implement $refs
3. Implement protobuf schema type form builder
4. Implement avro schema type form builder
   4.1. Fix array with items (example.avsc schema)
