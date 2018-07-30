pipeline {
  agent any
  stages {
    stage('Package') {
      steps {
        sh '''#!/bin/bash
          chmod +x package.sh
          ./package.sh
        '''
      }
    }
    stage('Archive artifacts') {
      steps {
        fileExists 'riaps-pycom-amd64.deb'
        archiveArtifacts(artifacts: 'riaps-pycom-amd64.deb', onlyIfSuccessful: true, fingerprint: true)
        fileExists 'riaps-pycom-armhf.deb'
        archiveArtifacts(artifacts: 'riaps-pycom-armhf.deb', onlyIfSuccessful: true, fingerprint: true)
        fileExists 'riaps-systemd-amd64.deb'
        archiveArtifacts(artifacts: 'riaps-systemd-amd64.deb', onlyIfSuccessful: true, fingerprint: true)
        fileExists 'riaps-systemd-armhf.deb'
        archiveArtifacts(artifacts: 'riaps-systemd-armhf.deb', onlyIfSuccessful: true, fingerprint: true)
      }
    }
  }
}
