# HSPyLib TODOs

## HSPYLIB

1. Check if execute SQLs, use params instead of values inside sql string.
2. Add a repository for SQLite db + tests.
3. Add a repository for Postgres db + tests.
4. Include a form validator for minput.
5. Improve tui -> extra with settings and remove parameters.
6. Fix README.md images and finish the documentation.
7. Replace setup.py: https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
8. Use virtual environments: https://www.geeksforgeeks.org/python-virtual-environment/

## HSPYLIB-FIREBASE

1. Rename firebase to fireblaze

## HSPYLIB-VAULT

1. Rename vault to volt
2. Add vault menu

## HSPYLIB-KAFMAN

1. Install Droid font with kafman pip install
    '''int id = QFontDatabase::addApplicationFont(":/SMSicons/segoeui_0.ttf");
    QString family = QFontDatabase::applicationFontFamilies(id).at(0);
    QFont _font(family, 8);
    qApp->setFont(_font);'''
2. Implement json schema type form builder
4. Add a button to find all topics
5. Add offset filters
6. Add a commit offset button
7. Add settings from all_settings.txt
