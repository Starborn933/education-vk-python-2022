properties([disableConcurrentBuilds()])

pipeline {
    agent {
        node {
            label 'master'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
        timestamps()
    }

    environment {
        VAR="123"
    }

    stages {

        stage("Build") {
            steps {
                echo 'building..'
                echo 'build done!'
            }
        }

        stage("Testing one ...") {
            steps {
                echo "one"
                sh "cd $WORKSPACE/lection19/code && pytest -s -l -v tests/test.py --alluredir ${WORKSPACE}/alluredir"
            }
        }

        stage("Testing two ...") {
            steps {
                echo "two"
                sh "cd $WORKSPACE/lection19/code && pytest -s -l -v tests/test_second.py --alluredir ${WORKSPACE}/alluredir"
            }
        }
    }

    post {
        always {
            allure([
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'alluredir']]
            ])
            cleanWs()
        }
    }
}
