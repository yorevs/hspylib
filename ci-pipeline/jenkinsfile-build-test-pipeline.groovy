#!/usr/bin/env groovy

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

  environment {
  }

  stages {

    stage('Pre Build Actions') {
      steps {
        prepareBuild()
      }
    }

    stage('Build') {
      steps {
        script {
          sh "./gradlew -g . clean build"
        }
      }
    }

    stage('Unit Tests') {
      steps {
        script {
          sh sh "./gradlew -g . check"
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
