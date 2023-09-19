# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][kac] and this project adheres to [Semantic Versioning][semver].

    [kac]: https://keepachangelog.com/en/1.0.0/
    [semver]: https://semver.org/

    ## Unreleased

    ### Added

    ### Fixed

    ### Updated

    ### Removed

## Unreleased

### Added

### Fixed

### Updated

### Removed

---

## v0.11.1 - 2022-12-06

### Added

* Added missing docs for public release.
* Added a new project datasource that was removed from the core library.
* Added Firebase security check.

### Fixed

* Fixed Various bugfixes

### Updated

* Updated Upgraded to gradle 7.4.2.
* Updated Vault now uses SQLite database instead of a simple file.
* Updated Kafman accept schemas.
* Updated Moved all applications to the new arguments framework.
* Updated publication docs.
* Updated Refactoring to match a final package structure.
* Updated Discontinued submodule versioner since bumpver already does what we need.

---

## v0.10.1 - 2021-05-03

### Added

* Added SendMsg widget.
* Added create widget mode for hspylib app.
* Added Pruni widget scratch.
* Added widgets manager.
* Added minput type "masked".
* Added minput type "select".
* Added versioner app draft.
* Added draft for git and versioning.
* Added unittests for application.
* Added docgen.gradle extension.
* Added py file headers.
* Added Time Calc widget.
* Added Terminal module.
* Added support for ini and yaml for Properties.
* Added dashboard icons.
* Added a unit test for application framework.
* Added docgen gradle extension - Non functional.
* Added Specialized exceptions and refactorings regarding it.
* Added hspylib manager app.
* Added mdashboard - scratch.
* Added PyLint and pylint cleanup.
* Added mdashboard demo.

### Fixed

* Fixed Code and pylint cleanup.
* Fixed setup to classify as Linux based kernels.
* Fixed menu_extra exit that was not re-showing cursor and ++version.
* Fixed input validators for minput
* Fixed minput to remove the mask after value was validated.
* Fixed Pylint errors.
* Fixed the position of the error message when validating the entire form.
* Fixed Bugfix version string in template.
* Fixed Small bugfix about appman.
* Fixed setup to match python guidelines.
* Fixed comments and exception tune.
* Fixed percent operation for calculator.
* Fixed vault, firebase and cfman according to the new application framework.
* Fixed name conventions.
* Fixed MDashboard bugfixes.
* Fixed some minor bugs.

### Updated

* Updated Improve minput to return an object with the fields instead of a dict.
* Updated Finished SendMsg widget. Improved with argument parser.
* Updated Doc headers, formatting, import optimize and adjustments on menu extra.
* Updated Additional improvements for menu -> extra.
* Updated Improved SendMsg widget.
* Updated Improved calc widget with masked input.
* Updated Moved keyboard to cli package.
* Updated Improved mselect and mchoose to match minput and mdashboard.
* Updated Renamed hspylib addins to addons.
* Updated Finished application FW.
* Updated Improved versioner.
* Updated Improved exceptions.
* Updated Improved cfman application.
* Updated Improved return types.
* Updated Reformat code + sync usage messages with sample.
* Updated docgen to avoid replacing existing headers.
* Updated Renamed addins to addons at manifest.md.
* Updated Renamed all enum packages to enums, to avoid the AttributeError (name shadowing).
* Updated hspylib app to use current dir instead of HOME folder and add a test template.
* Updated Properties upgrade.
* Updated Moving and renaming application module.
* Updated Moving usage and welcome messages to a separate file.
* Updated helps according to the new apps FW.
* Updated Upgrade gradle to 7.0.
* Updated Refactored main hspylib app to fit the new application FW.
* Updated Improve hspylib applications.
* Updated Improve parse parameters and options.
* Updated Improving app framework. Missing conditional arguments.
* Updated Restructured apps to match manager structure.
* Updated dependencies, that will not have any task due to new hspylib manager app.
* Updated Improved mdashboard.
* Updated Grant +x for main.py.
* Updated Application FW upgrade.
* Updated Improved logging.

### Removed

* Removed inner classes from minput
* Removed inner classes from dashboard
* Removed ui package, creating cli under modules. Creating add-ins for main hspylib app. Moving some other files into a proper place
* Removed main try catch blocks.

---

## v0.9.20 - 2021-05-03

### Added

* Added versioned app and versioning gradle extension.
* Add QtCalculator app.
* Added application framework.
* Added PCF Manager Application.
* Added font awesome.
* Added minput.
* Added mchoose.
* Added mselect.
* Added keyboard.
* Added emojis.
* Added vt100 package and files.
* Added new gradle extensions.
* Added Vault app.
* Added return types to methods and functions.
* Added vt100 colors.
* Added validators and company repo for phonebook demo.
* Added gradle task to find packages.

+ Added phonebook demo.

* Added hspylib demos.
* Added tests for file db.
* Added dynamic menus capacity.
* Added table_renderer.
* Added Firebase repository and tests.
* Added Firebase Agent App
* Added postgresql docker compose.
* Added log to mock server test.
* Added mock server tests.
* Added Repositories.
* Added mysql tests.
* Added docker.gradle and mysql_repository.
* Added Charset and ContentType.
* Added fetch tests.
* Added ServerMock, Fetch and WireMock.
* Added security module.
* Added eventbus tests.

### Changed

* Moved credentials from gradle file to environment variable.
* Moved TODO into doc folder.
* Improved library installation for publishing.
* Moved requirements per project and subproject.
* Moved VERSION to .version per project and subproject
* Removed app_endpoints.txt
* Updated apps to use the new app FW.
* Changed AppConfigs to make it subscript-able.
* Replaced all escape codes by Vt100 placeholders
* Moved RegexCommons to a separate file
* Created repository and service for vault
* Improved validations and refactorings
* Removed personal vault entries
* Renamed files to match convention.
* Service and Repository improvements.
* Deleted *.dat files.
* Improved TableRender by allowing adjustments on cell size.
* Updated MIT License.
* Updated cli menu.
* Refactorings to enable postgres. Removed sql factory facade.
* Properties and config updates.
* Improved execute, commit and rollback to db_repository.
* Separated gradle files.
* Fetch now uses requests instead of curl.
* Mock Server improvements.
* Separated mock_server_handler and request.
* Merged handler with server.
* Removed the gpg dependency, using python module cryptography.
* Improved gradle build.
* Gradle upgrade.
* Package improvements.
* Improved project structure.

### Fixed

* Skipped mysql tests.
* Fixed CF manager app.
* Fixed capital ignoring bug
* Fixed function wrappers.
* Fixed python.gradle build.
* Fixed formIcons post merge.
* Fixed phonebook demo.
* Mysql fixes and improvements.
* Fixed mselect when running at terminal (sysout not flushing).
* Fixed app when it throws errors.
* Fixed __init__ synchronization.
* Fixed Gradle build.
* Fixed setup.py to include sql files.
* Fixed module installation.
* Fixed logging problems and package moves.
* Fixed updateVersion task.
* Fixed install dependencies.
* Fixed many tests.
* Fixed charset and content-type.
* Fixed gradle build missing appdirs.
* Fixed both pycharm run and gradle run for tests.
* Fixed build.gradle.
* Fixed missing gradle stuff not running tests.

---

## 0.9.0 - 2020-05-28

### Added

* Initial version.
