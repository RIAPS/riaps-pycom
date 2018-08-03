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
    stage('Deploy') {
      when { buildingTag() }
      steps {
        // Install github-release cli tool to build directory
        sh 'GOPATH=$WORKSPACE/go go get github.com/aktau/github-release'
        // Use GitHub OAuth token stored in 'github-token' credentials
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          script {
            def user = 'riaps'
            def repo = 'riaps-pycom'
            def files = ['riaps-pycom-amd64.deb','riaps-pycom-armhf.deb','riaps-systemd-amd64.deb','riaps-systemd-armhf.deb']
            // Create release on GitHub, if it doesn't already exist
            sh "${env.WORKSPACE}/go/bin/github-release release --user ${user} --repo ${repo} --tag ${env.TAG_NAME} --name ${env.TAG_NAME} --pre-release || true"
            // Iterate over artifacts and upload them
            for(int i = 0; i < files.size(); i++){
              sh "${env.WORKSPACE}/go/bin/github-release upload -R --user ${user} --repo ${repo} --tag ${env.TAG_NAME} --name ${files[i]} --file ${files[i]}" 
            } 
          }
        }
      }
    }
  }
  post {
    success {
      archiveArtifacts artifacts: '*.deb', fingerprint: true
    }
  }
}
