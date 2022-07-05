/*
 * Gradle root build file
 *
 * This is a general purpose Gradle build.
 * Learn more about Gradle by exploring our samples at https://docs.gradle.org/7.0/samples
 * This file was generated by the HSPyLib appman.
 */

plugins {
  id 'idea'
  id "org.jetbrains.gradle.plugin.idea-ext" version "1.1.4"
}

idea {
  module {
    settings {
      rootModuleType = 'PYTHON_MODULE'
    }
    sourceDirs += file('src/main')
    testSourceDirs += file('src/test')
    excludeDirs += file('.idea')
    excludeDirs += file('.gradle')
    excludeDirs += file('.vscode')
    excludeDirs += file('src/main/build')
    excludeDirs += file('src/main/dist')
    excludeDirs += file('src/main/%APP_NAME%.egg-info')
  }
}

ext {
  python = "python${pythonVersion}"
  pyrcc = "pyrcc${pyrccVersion}"
  startTime = System.currentTimeMillis()
  verbose = findProperty('verbose') ?: false
  sourceRoot = "$rootDir/modules/$project.name/src"
  application = "$sourceRoot/main/__main__.py"
  pythonPath = "$sourceRoot/main:$sourceRoot/test:$sourceRoot/demo"
}

apply from: "$rootDir/gradle/dependencies.gradle"
apply from: "$rootDir/gradle/python.gradle"
apply from: "$rootDir/gradle/build-info.gradle"
apply from: "$rootDir/gradle/pypi-publish.gradle"
apply from: "$rootDir/gradle/docker.gradle"
apply from: "$rootDir/gradle/badges.gradle"
apply from: "$rootDir/gradle/docgen.gradle"

/* Run Configurations */
task exportRunConfigurations(type: Copy) {
  group = 'Idea'
  description = "Export run configurations"
  from("${rootDir}/.idea/runConfigurations") {
    include '*.xml'
  }
  into "${rootDir}/run-configs/idea"
}

task importRunConfigurations(type: Copy) {
  group = 'Idea'
  description = "Import run configurations"
  from("${rootDir}/run-configs/idea") {
    include '*.xml'
  }
  into "${rootDir}/.idea/runConfigurations"
}
