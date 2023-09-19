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

* Added .idea folder.
* Added API documentation draft.
* Added Create Github actions  python-app.yml.
* Added Del and fit text to status bar.
* Added ExitCode to shell exec.
* Added Firebase config debug.
* Added Jenkins docker-compose.
* Added Kafman app - draft.
* Added Pruni widget scratch.
* Added Published first version of setman.
* Added QT Demos for promoted widgets.
* Added README and LICENSE to all modules.
* Added README.md to the version updates.
* Added Redis repository.
* Added SendMsg widget.
* Added Terminal demo.
* Added _config.yml.
* Added a code workspace.
* Added add topics button.
* Added api docs, reformagt code and organize imports.
* Added argument chain.
* Added astradb docker-compose (cassandra).
* Added avro form to json.
* Added build-test ci pipeline.
* Added build.gradle and build files for all apps.
* Added cache package, moved ttl_keyring_br to cache and created a ttl cache based on keyring. Added cfman app and space caches.
* Added cassandra repository.
* Added cfman blue/green check.
* Added clear form and txt toggle button.
* Added clitt settings export.
* Added collection filter tests.
* Added comments to py files.
* Added console_streamer, fix kafman thread problems.
* Added consumer events to the table.
* Added context menu for hlistwidget.
* Added context menu to delete rows.
* Added create widget mode for hspylib app.
* Added droid font to installation.
* Added equality operator __eq__.
* Added export form to producer text.
* Added fetch tests and improved fetch. Upgraded Kafman to customize schema registry url.
* Added game icons and some icon improvements.
* Added github funding files.
* Added idea plugin.
* Added input type masked.
* Added input validation for firebase setup.
* Added json schema.
* Added json type schema format cont....
* Added json type schema format.
* Added kafka docker-compose.
* Added kafka package and some improvements.
* Added kafman ability to commit offset and custom menus for htableview.
* Added keyring to store the passwd in keyring for ttl minutes (now 15m).
* Added line numbers and line highlight to hconsole.
* Added local install "dev mode".
* Added misc docs -> awesome icons csv.
* Added mypy check task. For now it is a separate task.
* Added new datasource module. Removing from root library.
* Added offset filters.
* Added pdoc auto doc api.
* Added postgres repository.
* Added preconditions to replace the asserts.
* Added producer form.
* Added publish task changelog.
* Added py file headers and reformat files.
* Added pydocs and adjustments.
* Added pydocs and small fixes - part1.
* Added pydocs and small fixes - part7.
* Added pydocs, smalls bugfixes and change some Any to the proper type.
* Added python headers and organize imports according to isort.
* Added registry server manipulation.
* Added run pycharm run configurations.
* Added schema form validation.
* Added settings source (bash export).
* Added sorting to htablemodel.
* Added sql filters and fix vault.
* Added statistics to Kafman.
* Added support for toml files.
* Added terminal module - scratch.
* Added tests for text_tools and fixed kafman minor issues.
* Added the SchemaFactory and registry information.
* Added the option to truncate by passing stype.
* Added threads to producer and consumer.
* Added tooltips, placeholders and adjustments.
* Added update hspylib version and avoid copying README from rootDir into modules.
* Added vault tui when editing and fixed datasource execute with parameters.
* Added versioner app draft.

### Fixed

* Fixed @package at headers.
* Fixed Bugfix version string in template.
* Fixed Bugfix: vault anb clitt.
* Fixed Bugfixes - minput tokenized.
* Fixed Bugfixes Kafman and HsPyLib.
* Fixed Bugfixes and fix tests.
* Fixed Bugfixes on demos.
* Fixed Bugfixes, improvements and additional hstackedwidget.
* Fixed Bugfixes, improvements, refactorings and auto docs.
* Fixed Firebase agent config and republich all.
* Fixed Firebase setup -> Properties -> Datasource configs.
* Fixed Firebase setup not writing properties.
* Fixed Firebase.
* Fixed Kafman core dump problem due to different thread.
* Fixed Minor menu extra fixes.
* Fixed Phonebook bugfixes.
* Fixed Small bugfix about appman and finished first version of docgen gradle extension.
* Fixed Terminal.poll and moved Keyboard.py back to hspylib core.
* Fixed URL builder and fetch fixes.
* Fixed Versioner.
* Fixed VtCodes bugfixes. enum.cls.names filter repeated values since python 3.11.
* Fixed after refactorings.
* Fixed and add preserve to Setman and settings.
* Fixed and enable mchoose,mselect to export to file.
* Fixed and enable minput to export to file.
* Fixed and improved the config properties.
* Fixed and publish vault and firebase.
* Fixed and pylint cleanup.
* Fixed app_config creating application.properties file.
* Fixed app_config param resourse_dir removal.
* Fixed application::getarg fixes.
* Fixed appman addon.
* Fixed appman and widgets.
* Fixed array/enum for jsonschema.
* Fixed avro schema (type AVRO).
* Fixed avro schema parsing and form building.
* Fixed avro.errors due to new version.
* Fixed awesome icons.
* Fixed bugfixes including changing LOG_DIR to HHS_LOG_DIR.
* Fixed build and versions. Published the new versions.
* Fixed build badges.
* Fixed build pipeline.
* Fixed cfman and add new tui preferences. Also small fix to clitt.
* Fixed cfman and some minor visual improvements.
* Fixed cfman split in tuple.
* Fixed cfman.
* Fixed clitt table_renderer, upgrade setman to allow prefixes.
* Fixed clitt widgets.
* Fixed compilation problems due to renaming menu.extra to ui.extra.
* Fixed core dump due to missing model.column() method.
* Fixed data folders.
* Fixed dependencies and removing pipreqs from gradle builds.
* Fixed dependencies issues.
* Fixed dependency problems and change the dependency gradle to allow using version and space to install [@hjunior].
* Fixed docker scripts.
* Fixed docker-composes and start/styop scripts.
* Fixed excluded directories.
* Fixed fetch/kafman bugfixes.
* Fixed file not found on firebase dto save.
* Fixed firebase and vault. Added clitt dependency.
* Fixed firebase bug when file to upload was not found and add except for application InvalidStateError.
* Fixed firebase little config bugs.
* Fixed firebase_config from hspylib and firebase module.
* Fixed for all projects after gradle changes.
* Fixed form change problems due to reference issues.
* Fixed globbing.
* Fixed gradle installModule as dev mode.
* Fixed gradle tasks calling clean all the time.
* Fixed hqt package structure.
* Fixed hspylib app and improve application fw.
* Fixed hspylib applications using wrong resource_dir.
* Fixed hspylib appman.
* Fixed hspylib commons fixes and setman improvements/fixes.
* Fixed hspylib create qt-app.
* Fixed hspylib widgets addon.
* Fixed idea run configurations and move back vt100 module to hspylib.
* Fixed imports.
* Fixed input validator anything regex bug.
* Fixed input validators for minput.
* Fixed install build tools and add run-configs.
* Fixed kafman fonts when user does not have it installed.
* Fixed kafman table filters.
* Fixed last datetime.now references.
* Fixed logging (remove default root logger). Updated hspylib appman to create a qt application.
* Fixed menu_extra exit that was not re-showing cursor and ++version.
* Fixed minput -> camelcase the lower label.
* Fixed minput to remove the mask after value was validated.
* Fixed mselect,mchoose and minput when result is none.
* Fixed package and test problems.
* Fixed packages after modularization.
* Fixed packages and install routines.
* Fixed packaging part - 2.
* Fixed pre-pylint.
* Fixed pre-release.
* Fixed problem when docker command fails.
* Fixed punch.
* Fixed pylint gradle tasks.
* Fixed pylint violations.
* Fixed pypi install/run problems due to classpaths.
* Fixed python clean targets.
* Fixed python paths and tests.
* Fixed reformat, refactorings (move kafka from main). Improve kafman form (not done yet).
* Fixed required producer and consumer settings.
* Fixed ret_val = None bug.
* Fixed run configurations.
* Fixed run.sh scripts.
* Fixed sample.vault mess.
* Fixed schema loading (register).
* Fixed schema.name -> schema.fullname according to new avro lib.
* Fixed send_msg widget.
* Fixed serialization settings for producer and consumer.
* Fixed some bugs on the Kafman UI.
* Fixed some demos due to package changes.
* Fixed some tests and the hash problem of the enumeration.
* Fixed stacked panel contents.
* Fixed sync headers line break.
* Fixed sysout problems when none comes in.
* Fixed tests and test packages.
* Fixed text_tools issues.
* Fixed the Kafka Registry/ControlCenter docker integration.
* Fixed the imports.
* Fixed the position of the error message when validating the entire form.
* Fixed the vault backup filename.
* Fixed timecalc widget add ESC[ characters to the output due to sysout.
* Fixed to improve code quality.
* Fixed unit tests and pylint stuff.
* Fixed vault listing filters.
* Fixed vault tui integration for add and upd.

### Updated

* Updated doc headers and some fixes.
* Updated setman to display environ_name and add empty pyproject.toml.
* Updated the application argument parser.
* Updated Accept multiple schema files to choose.
* Updated Additional improvements for menu -> extra.
* Updated Adjust __init__ and create setup.py for all apps.
* Updated Adjust setup to classify as Linux based kernels.
* Updated Adjust the version and modified date for files.
* Updated Adjust versions to match latest clitt version.
* Updated Adjustments before adding SchemaFactory.
* Updated Adjustments before adding schemas.
* Updated Animated qtoolbox.
* Updated Api docs, code reformat and organize imports.
* Updated Application and QtApplication framework tweaks.
* Updated Application execution adjustments and fixes.
* Updated Application refactorings.
* Updated Appman with menu input and fixes.
* Updated Attempt to use schema registry on docker.
* Updated Avoid adding dups to combo topics.
* Updated CFMan -> Clitt bugfixes.
* Updated CRUD Refactoring - part 1.
* Updated Calculator refinements.
* Updated Change Firebase repository to match the API.
* Updated Change docgen to avoid replacing existing headers.
* Updated Change formatter skip from @formatter to fmt to use black formatter.
* Updated Change syncPythonPackages to skipmodules starting with __.
* Updated Code and pylint cleanup.
* Updated Code reformat using black formatter.
* Updated Consolidated Kafka Docker and schemas.
* Updated Create new icons category and fix end_ln.
* Updated Creating 1 class per avro type.
* Updated Disallowing serialization and serialization settings from add setting.
* Updated Doc headers to new files and adjustments.
* Updated Doc headers, formatting, import optimize and adjustmets on menu extra.
* Updated Docker improvements and healthchecks.
* Updated Docker scripts fixups.
* Updated Docker.gradle upgrades.
* Updated Enable add settings from kafka settings in a a dialog.
* Updated Fetch is_reachable bugfixes.
* Updated Final resourse dir and version fixes.
* Updated Finish Qt Promotions Demo and some refactorings. Re-Publish all modules after library update.
* Updated Finish application FW and improve versioner.
* Updated Finish gradle docgen extension.
* Updated Finish time calc widget.
* Updated Finished Setman implemntation.
* Updated Finished Terminal module and improved cfman.
* Updated Firebase setup.
* Updated Firebase to allow uploading empty files.
* Updated Firebase will allow globbing.
* Updated First kafman working version.
* Updated First working version.
* Updated Freeze dependencies.
* Updated Github actions - 1.
* Updated Gradle script improvements.
* Updated HStackedWidget was not auto-resizing to the new form.
* Updated Implement find all topics of broker.
* Updated Implementation of TUIScreen - draft.
* Updated Improing widgets addin. First working version.
* Updated Include import/export features to setman.
* Updated Include table_renderer footer.
* Updated Input validator and more refactorings.
* Updated Installation fixes.
* Updated JsonSchema parsing. Now its just missing the reference parsing.
* Updated Kafman improvements, new ui promotions and fixes.
* Updated Kafman: Add avro schema - draft.
* Updated Kafman: Updating HConsole based on c-rial. Fixups, adding a delay to refresh the console.
* Updated Kafmand: Improved the way consumer and producer work and allow both to run.
* Updated Line numbers and highlight fixes.
* Updated Log adjustments.
* Updated Mention JetBrains on README.md.
* Updated Menu -> Extra refactorings and improvements.
* Updated Migrate apps to the new argument framework.
* Updated Migrate into ArgumentParser.
* Updated Minput and Widgets adjustments.
* Updated More icons. Kafman: added clearable and context menu enable.
* Updated Move applications framework out of cli package.
* Updated Moved QT demod to qt package.
* Updated Moved all setman/settings from clitt into a new pypi/gradle project.
* Updated Moved some docs to docs folder and add main index.html api docs.
* Updated Moving apps into modules directory to modularize the library.
* Updated Moving constants and preconditions out of tools package.
* Updated Moving date and time constants to zoned_datetime.
* Updated Moving regex constants from class to root.
* Updated New Kafman icon.
* Updated Normalize project name to HsPyLib.
* Updated Preparation for record form field parsing.
* Updated Preparation to fix avro schema parsing and form building.
* Updated Prepared main ui to receive the new schema form.
* Updated Prevent source and test folders to be wiped out by gradle plugin.
* Updated Promote widgets and first working version.
* Updated Pruni widget.
* Updated Publish all modules again.
* Updated Publish hspylib and firebase.
* Updated Punch Widgets.
* Updated README and other docs.
* Updated README.md with DigitalOcean link.
* Updated README.md with examples.
* Updated Refactoring some commons functions.
* Updated Refactoring to allow many schemas.
* Updated Refactoring to match a final package structure.
* Updated Refactorings and doc updates.
* Updated Refactorings and fixes: gradle and Kafman.
* Updated Refactorings and improvements.
* Updated Refactorings before changing CRUD files.
* Updated Refactorings, add final namespace, add abstract singleton.
* Updated Refactorings, adding pydocs and small fixes.
* Updated Refactorings, fix python3.10 errors, add widget punch(draft) add firebase auth.
* Updated Refactorings: Removing ui package, creating cli under modules. Creating add-ins for main hspylib app. Moving some other files into a proper place.
* Updated Reformat code + sync usage messages with sample..
* Updated Rename SchemaFieldType to AvroType.
* Updated Rename from regex_constants to constants.
* Updated Rename hspylib addins to addons and fix widgets find_widget.
* Updated Renames according to demo and fix packages - part1.
* Updated Renames and repackaging.
* Updated Renaming all enum packages to enums, to avoid the AttributeError.
* Updated Renaming all run-it.sh to run.sh.
* Updated Replace bumpversion by bumpver.
* Updated Republish all modules to fix the urllib requirements.
* Updated Revert "Fix hspylib applications using wrong resource_dir".
* Updated SendMsg widget.
* Updated Separate qt module into a new project : hqt.
* Updated Separate the TUI module from the library. Moved into a new project: clitt.
* Updated Set all icons as composable.
* Updated Setman -> Settings.
* Updated Setup adjustments, renamed addins to addons at manifest.md.
* Updated Sync requirements and gradle updates for it.
* Updated TODOS.
* Updated TODOs, added draft for git and versioning.
* Updated TODOs.
* Updated TUI Improvement: improving minput with correct input and field validators.
* Updated TUI Improvement: integration with the new TUIScreen - part1.
* Updated TUI Improvement: integration with the new TUIScreen - phonebook.
* Updated TUI module - part 1.
* Updated TUIPreferences.
* Updated TUIScreen improvement and add a demo for it.
* Updated Terminal and screen bigg refactorings.
* Updated Toggle between code and form is now possible.
* Updated Typing the return of the TUI components.
* Updated UI Refinements and glitch fixes.
* Updated Update Kafman: Add preparation for schemas.
* Updated Updated Finished SendMsg widget. Improved with argument parser.
* Updated Updated Visual improvements (print settings, warn box, etc).
* Updated Use PyPi token instead of un/pw.
* Updated Use the __classpath__ approach in all hspylib apps.
* Updated Using context lib to open/close the vault.
* Updated Using findProperty and ?: instead of hasProperty.
* Updated Vault now creates a backup. ++Bugfixes.
* Updated Vault using env for passphrase.
* Updated AUTO updated build & check badges.
* Updated Improve build-test github action.
* Updated all apps with the new application framework.
* Updated and fix cfman and allow action to be passed to build args.
* Updated and fix vault app.
* Updated application framework.
* Updated badges.gradle.
* Updated build install actions.
* Updated build speed by using requirements field to install all dependencies and tools.
* Updated build-test actions.
* Updated comments and pydocs.
* Updated copyright.
* Updated databus and kafman.
* Updated default settings.
* Updated detect user space by checking for venv.
* Updated doc headers, refactorings, reformat. Modev Kafka code away from library.
* Updated docker containers.
* Updated docs , version and move keyboard to cli package.
* Updated documents and moved into root folder.
* Updated dynamic schema form.
* Updated editorconfig.
* Updated eventbus module.
* Updated file headers.
* Updated firebase setup by using clitt uis.
* Updated form icons and add minput tooltips.
* Updated git hooks.
* Updated gradle files to modularize the library.
* Updated gradle files to support multi-project.
* Updated headers.
* Updated icons.
* Updated improve calc widget with masked input.
* Updated improvement and fixes. Add elidable hlabel.
* Updated installModule to install local package for development.
* Updated kafka docker compose and examples.
* Updated menu extra refinements.
* Updated minput to return an object with the fields instead of a dict.
* Updated minput with the mode "select".
* Updated mselect and mchoose to match minput and mdashboard.
* Updated oracle.gradle.
* Updated pre producer form.
* Updated publication docs.
* Updated pypi publish method to use build package.
* Updated qt components and Kafman.
* Updated qt_view to find all widgets automatically; removed qt_finder then.
* Updated renaming some test files.
* Updated run configurations with setman.
* Updated run-configs.
* Updated schema registry.
* Updated setman - first working version almost ready.
* Updated setman display messages.
* Updated setman/settings - part1.
* Updated setman/settings - part2.
* Updated setman/settings adding cache.
* Updated setman/settings bugfixes.
* Updated setman/settings import/export CSV.
* Updated setup.py.
* Updated some exceptions.
* Updated some gradle scripts.
* Updated syncPythonHeaders now is finalized by optimize imports.
* Updated table_renderer with more adjustments and performance.
* Updated the Firebase access by removing UUID, allowing single entry downloads and dir uploads.
* Updated the copyright note.
* Updated the dependency management gradle.
* Updated the line highlight and numbers.
* Updated the schema form fields.
* Updated the version number.
* Updated unittests for application.
* Updated upgrade to gradle 7.4.2.
* Updated vault get by name.
* Updated vault to use sqlite instead of normal file - part 1.
* Updated version number.
* Updated versioner and fix-ups.
* Updated versioner to be used in future versions of hspylib.
* Updated versions to match the new requirements files.
* Updated versions.
* Updated versions.
* Updated widgets manager scratch.

### Removed

Removed .idea files.
Removed Discontinued submodule versioner.
Removed Jenkins pipelines.
Removed Pruni, added tcalc. Fixed Widgets bugs.
Removed all asserts.
Removed context, open, close and encoding database..
Removed firebase details from being displayed.
Removed gradle.bat.
Removed ide files.
Removed inner classes from dashboard.
Removed inner classes from minput.
Removed log init from app_configs and some tunes and fixes for application FW.
Removed manual schema register since value.subject.name.strategy is not exposed on Python.
Removed passphrase from firebase_config.
Removed postgres from datasource project.
Removed print requirements from setup.py.
Removed pylint warnings.
Removed scope from hspd files.
Removed warnings.

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
