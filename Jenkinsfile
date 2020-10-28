pipeline {
  agent { label 'docker' }
  environment {
        REGISTRY = 'bluehost-docker-stage-awsuseast.artifactory.svcs.endurance.com/bluehost-docker-stage/'
    }
  stages {
        stage('Set Env') {
            steps {
                sh "cp ${workspace}/files/dev .env"
            }
        }
        stage('Prepare') {
            steps {
                sh "echo Prepare"
                sh "docker-compose rm -f -s -v"
            }
        }
        stage('Build') {
            steps {
                sh "docker-compose up --build -d"
            }
        }
        stage('Test') {
            steps {
		        //sh "pip install pytest flask_jwt_extended requests"
		        sh "docker ps --filter health=healthy"
		        sh "sleep 1m"
		        sh "docker ps --filter health=healthy"
                //sh "pytest ${workspace}/tests/integration_tests/"
            }
        }
        stage('Deploy') {
            steps {
                sh "echo Deploy"
                //sh "cd ${workspace}; devpi upload"
            }
        }
        stage('Upload build to Artifactory') {
            steps {
                script {
                    docker.withRegistry("https://${env.REGISTRY}/", 'SVC') {
                            docker.image("deployment/deployment_proxy:latest").push() }
                }
            }
        }
  }
  post {
    always {
      echo 'This will always run'
      sh "echo Cleanup"
      sh "docker-compose rm -f -s -v"
      script {
        echo "Pipeline result: ${currentBuild.result}"
        echo "Pipeline currentResult: ${currentBuild.currentResult}"
        notifyBitbucket()
      }
    }
    success {
      echo 'This ran because the pipeline was successful'
    }
    failure {
      echo 'This ran because the pipeline failed'
    }
    unstable {
      echo 'This ran because the pipeline was marked unstable'
    }
    changed {
      echo 'This ran because the state of the Pipeline has changed'
      echo 'For example, if the Pipeline was previously failing but is now successful'
    }
  }
}
