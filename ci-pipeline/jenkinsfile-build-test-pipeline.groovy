#!/usr/bin/env groovy

def allModules = [
  'cfman',
  'clitt',
  'datasource',
  'firebase',
  'hspylib',
  'kafman',
  'setman',
  'vault'
]

pipeline {
  agent {
    node {
      // Alpine JDK-11 and Python v3.11.5
      label 'docker-agent-python3'
    }
  }

  options {
    ansiColor('xterm')
  }

  stages {

    stage('Pre Build Actions') {
      steps {
        prepareBuild()
      }
    }

    stage('Build') {
      failFast true
      parallel {
        stage('HSPyLib - Core') {
          steps {
            script {
              allModules.each { module ->
                sh "./gradlew -g . ${module}:clean ${module}:buildOnly ${params.gradle_debug_params}"
              }
            }
          }
        }
      }
    }

    stage('Install and Test') {
      failFast true
      parallel {
        stage('HSPyLib - Core') {
          steps {
            script {
              allModules.each { module ->
                sh "./gradlew -g . ${module}:installModule ${module}:check ${params.gradle_debug_params}"
              }
            }
          }
        }
      }
    }

  }

  post {
    always {
      // Delete the workspace after build is finished.
      deleteDir()
    }
  }
}

def prepareBuild() {
  script {
    // readProperties -> Ref:. https://github.com/jenkinsci/pipeline-utility-steps-plugin/blob/master/docs/STEPS.md
    def props = readProperties file: 'gradle.properties'
    props.each { p ->
      print("info: WITH PROPERTY: ${p}")
    }

    print("info: BUILD_TOOLS=${props['buildTools']}")
    print("info: PYTHON_VERSION=${props['pythonVersion']}")
    print("info: PYRCC_VERSION=${props['pyrccVersion']}")
  }
}
