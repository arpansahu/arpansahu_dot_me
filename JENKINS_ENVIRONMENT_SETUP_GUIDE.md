# Jenkins Environment Variable Centralization Guide

## Overview
This guide documents how to centralize environment variables in `.env` file and fix Jenkins pipeline permission issues. Apply these patterns to other Django/Docker projects with Jenkins CI/CD.

---

## Problem Statement

### Issues We Fixed:
1. **Permission Errors**: Jenkins couldn't create `.env` file using shell commands (`cp`, `cat` with redirection)
2. **Hardcoded Values**: Docker registry, deployment configs scattered across Jenkinsfiles
3. **Variable Duplication**: Same values repeated in multiple places
4. **Configuration Complexity**: 7+ deployment variables when only 4 base variables needed

---

## Solution Architecture

### Key Principles:
1. **Single Source of Truth**: All configuration in `.env` file
2. **Derived Variables**: Compute values programmatically from base variables
3. **Jenkins Native APIs**: Use `readFile()`/`writeFile()` instead of shell commands
4. **Fail Fast**: Validate required variables early in pipeline

---

## Step-by-Step Implementation

### 1. Centralize Docker Registry Configuration

#### Before (Hardcoded):
```groovy
// In Jenkinsfile-build
environment {
    DOCKER_REGISTRY = 'harbor.arpansahu.space'
    DOCKER_REPOSITORY = 'library'
    DOCKER_IMAGE_NAME = 'arpansahu_dot_me'
}
```

#### After (.env file):
```bash
# .env
DOCKER_REGISTRY=harbor.arpansahu.space
DOCKER_REPOSITORY=library
DOCKER_IMAGE_NAME=arpansahu_dot_me
DOCKER_IMAGE_TAG=latest
```

#### Update Jenkinsfile:
```groovy
// Remove from environment{} block, load in Setup Environment stage
stage('Setup Environment') {
    steps {
        script {
            withCredentials([file(credentialsId: 'your_env_file_credential', variable: 'ENV_FILE')]) {
                // Use Jenkins API instead of shell commands
                def envContent = readFile(file: env.ENV_FILE)
                writeFile(file: '.env', text: envContent)
                echo '.env file created successfully from credentials'
                
                // Parse and load environment variables
                def envVars = sh(script: 'cat .env | grep -v "^#" | grep -v "^$" | xargs', returnStdout: true).trim()
                if (envVars) {
                    envVars.split().each { envVar ->
                        if (envVar.contains('=')) {
                            def parts = envVar.split('=', 2)
                            def key = parts[0]
                            def value = parts.length > 1 ? parts[1] : ''
                            if (key) {
                                env."${key}" = value
                            }
                        }
                    }
                }
                
                // Compute derived variables
                env.REGISTRY = "${env.DOCKER_REGISTRY}/${env.DOCKER_REPOSITORY}"
                env.REPOSITORY = "${env.DOCKER_REGISTRY}/${env.DOCKER_REPOSITORY}/${env.DOCKER_IMAGE_NAME}"
                
                echo "Docker Image: ${env.REPOSITORY}:${env.BUILD_NUMBER}"
            }
        }
    }
}
```

### 2. Reduce Variable Duplication with Smart Derivation

#### Before (.env had):
```bash
ENV_PROJECT_NAME=arpansahu_dot_me
BUILD_PROJECT_NAME=arpansahu_dot_me_build
PROJECT_NAME_WITH_DASH=arpansahu-dot-me
NGINX_CONF_PATH=/etc/nginx/sites-available/arpansahu-dot-me
```

#### After (only base variable):
```bash
ENV_PROJECT_NAME=arpansahu_dot_me
```

#### Compute Derived Variables in Pipeline:
```groovy
// In Setup Environment stage
env.BUILD_PROJECT_NAME = "${env.ENV_PROJECT_NAME}_build"
env.PROJECT_NAME_WITH_DASH = env.ENV_PROJECT_NAME.replace('_', '-')
env.NGINX_CONF_PATH = "/etc/nginx/sites-available/${env.PROJECT_NAME_WITH_DASH}"

echo "Computed BUILD_PROJECT_NAME: ${env.BUILD_PROJECT_NAME}"
echo "Computed PROJECT_NAME_WITH_DASH: ${env.PROJECT_NAME_WITH_DASH}"
echo "Computed NGINX_CONF_PATH: ${env.NGINX_CONF_PATH}"
```

### 3. Fix Jenkins Permission Errors

#### ❌ WRONG - Shell Commands (Permission Issues):
```groovy
// DON'T DO THIS - fails in concurrent workspaces
sh "cp \$ENV_FILE .env"
sh "cat \$ENV_FILE > .env"
```

#### ✅ CORRECT - Jenkins Native APIs:
```groovy
// Use Jenkins readFile/writeFile APIs
def envContent = readFile(file: env.ENV_FILE)
writeFile(file: '.env', text: envContent)
```

**Why This Works:**
- Jenkins APIs have proper workspace permissions
- Works in concurrent workspaces (`@2`, `@3`, etc.)
- No shell redirection issues
- Platform-agnostic (works on Linux, Windows, macOS agents)

### 4. Update docker-compose.yml

#### Before:
```yaml
services:
  web:
    image: harbor.arpansahu.space/library/arpansahu_dot_me:latest
```

#### After:
```yaml
services:
  web:
    image: ${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
```

### 5. Update Kubernetes Deployment Scripts

#### Before (deploy_kube.sh):
```bash
#!/bin/bash
IMAGE_NAME="harbor.arpansahu.space/library/arpansahu_dot_me:latest"
kubectl set image deployment/arpansahu-dot-me web=$IMAGE_NAME
```

#### After:
```bash
#!/bin/bash

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Validate required variables
if [ -z "$DOCKER_REGISTRY" ] || [ -z "$DOCKER_REPOSITORY" ] || \
   [ -z "$DOCKER_IMAGE_NAME" ] || [ -z "$DOCKER_IMAGE_TAG" ]; then
    echo "Error: Missing required Docker registry variables"
    exit 1
fi

# Build full image name
IMAGE_NAME="${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

# Deploy
kubectl set image deployment/${PROJECT_NAME_WITH_DASH} web=$IMAGE_NAME
```

### 6. Create/Update env.example Template

```bash
# env.example - Template for required environment variables

# ============================================
# Docker Registry Configuration
# ============================================
DOCKER_REGISTRY=
DOCKER_REPOSITORY=
DOCKER_IMAGE_NAME=
DOCKER_IMAGE_TAG=

# ============================================
# Deployment Configuration
# ============================================
ENV_PROJECT_NAME=
SERVER_NAME=
DOCKER_PORT=
JENKINS_DOMAIN=

# ============================================
# Database Configuration
# ============================================
DATABASE_URL=

# ============================================
# Redis Configuration
# ============================================
REDIS_CLOUD_URL=

# ============================================
# Email Configuration (Mailjet)
# ============================================
MAIL_JET_API_KEY=
MAIL_JET_API_SECRET=

# ============================================
# OAuth Credentials
# ============================================
GITHUB_KEY=
GITHUB_SECRET=
TWITTER_KEY=
TWITTER_SECRET=
GOOGLE_KEY=
GOOGLE_SECRET=
LINKEDIN_KEY=
LINKEDIN_SECRET=

# ============================================
# Error Tracking (Sentry)
# ============================================
SENTRY_DSN=
SENTRY_ORG=
SENTRY_PROJECT=
SENTRY_AUTH_TOKEN=

# ============================================
# Object Storage (MinIO/S3)
# ============================================
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_ENDPOINT_URL=
AWS_S3_CUSTOM_DOMAIN=

# ============================================
# Django Configuration
# ============================================
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
```

### 7. Jenkins Credentials Setup

1. **Go to Jenkins Dashboard** → Manage Jenkins → Credentials
2. **Add File Credential**:
   - Kind: `Secret file`
   - File: Upload your `.env` file
   - ID: `project_name_env_file` (e.g., `arpansahu_dot_me_env_file`)
   - Description: `Environment variables for project_name`

3. **Add Docker Registry Credentials**:
   - Kind: `Username with password`
   - Username: `admin` (or your registry username)
   - Password: Your registry password
   - ID: `harbor-credentials` (or appropriate name)

### 8. Complete Jenkinsfile-build Template

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'project_name_env_file', variable: 'ENV_FILE')]) {
                        // Read and write .env file using Jenkins API
                        def envContent = readFile(file: env.ENV_FILE)
                        writeFile(file: '.env', text: envContent)
                        echo '.env file created successfully from credentials'
                        
                        // Load environment variables from .env
                        def envVars = sh(script: 'cat .env | grep -v "^#" | grep -v "^$" | xargs', returnStdout: true).trim()
                        if (envVars) {
                            envVars.split().each { envVar ->
                                if (envVar.contains('=')) {
                                    def parts = envVar.split('=', 2)
                                    def key = parts[0]
                                    def value = parts.length > 1 ? parts[1] : ''
                                    if (key) {
                                        env."${key}" = value
                                    }
                                }
                            }
                        }
                        
                        echo '✅ Environment variables loaded from .env'
                        
                        // Compute derived variables
                        env.BUILD_PROJECT_NAME = "${env.ENV_PROJECT_NAME}_build"
                        env.PROJECT_NAME_WITH_DASH = env.ENV_PROJECT_NAME.replace('_', '-')
                        env.REGISTRY = "${env.DOCKER_REGISTRY}/${env.DOCKER_REPOSITORY}"
                        env.REPOSITORY = "${env.DOCKER_REGISTRY}/${env.DOCKER_REPOSITORY}/${env.DOCKER_IMAGE_NAME}"
                        
                        echo "Computed BUILD_PROJECT_NAME: ${env.BUILD_PROJECT_NAME}"
                        echo "Computed PROJECT_NAME_WITH_DASH: ${env.PROJECT_NAME_WITH_DASH}"
                        echo "Docker Image: ${env.REPOSITORY}:${env.BUILD_NUMBER}"
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo 'Running Django Unit Tests...'
                    sh """
                        docker run --rm \
                            -v \$(pwd):/app \
                            -w /app \
                            --env-file .env \
                            python:3.9.6 bash -c "\
                                pip install -q -r requirements.txt && \
                                pip install -q pytest pytest-django pytest-cov && \
                                python -m pytest -m 'not ui' --ignore=tests -v"
                    """
                    echo '✅ All unit tests passed successfully!'
                }
            }
        }
        
        stage('Build Image') {
            steps {
                script {
                    sh "docker --version"
                    echo "Building Docker image: ${env.REPOSITORY}:${env.BUILD_NUMBER}"
                    sh "docker build -t ${env.REPOSITORY}:${env.BUILD_NUMBER} ."
                    sh "docker tag ${env.REPOSITORY}:${env.BUILD_NUMBER} ${env.REPOSITORY}:latest"
                }
            }
        }
        
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-credentials', 
                                                   usernameVariable: 'DOCKER_REGISTRY_USERNAME',
                                                   passwordVariable: 'DOCKER_REGISTRY_PASSWORD')]) {
                    script {
                        sh """
                            echo \$DOCKER_REGISTRY_PASSWORD | docker login ${env.DOCKER_REGISTRY} -u \$DOCKER_REGISTRY_USERNAME --password-stdin
                            docker push ${env.REPOSITORY}:${env.BUILD_NUMBER}
                            docker push ${env.REPOSITORY}:latest
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                // Send success notification
                echo "✅ Build ${env.BUILD_NUMBER} successful"
            }
        }
        failure {
            script {
                // Send failure notification
                echo "❌ Build ${env.BUILD_NUMBER} failed"
            }
        }
    }
}
```

### 9. Complete Jenkinsfile-deploy Template

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'DEPLOYMENT_TYPE', choices: ['docker', 'kubernetes'], description: 'Choose deployment type')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'project_name_env_file', variable: 'ENV_FILE')]) {
                        // Read and write .env file using Jenkins API
                        def envContent = readFile(file: env.ENV_FILE)
                        writeFile(file: '.env', text: envContent)
                        echo '.env file created successfully from credentials'
                        
                        // Load environment variables from .env
                        def envVars = sh(script: 'cat .env | grep -v "^#" | grep -v "^$" | xargs', returnStdout: true).trim()
                        if (envVars) {
                            envVars.split().each { envVar ->
                                if (envVar.contains('=')) {
                                    def parts = envVar.split('=', 2)
                                    def key = parts[0]
                                    def value = parts.length > 1 ? parts[1] : ''
                                    if (key) {
                                        env."${key}" = value
                                    }
                                }
                            }
                        }
                        
                        // Compute derived variables
                        env.BUILD_PROJECT_NAME = "${env.ENV_PROJECT_NAME}_build"
                        env.PROJECT_NAME_WITH_DASH = env.ENV_PROJECT_NAME.replace('_', '-')
                        env.NGINX_CONF_PATH = "/etc/nginx/sites-available/${env.PROJECT_NAME_WITH_DASH}"
                        
                        echo "Project: ${env.ENV_PROJECT_NAME}"
                        echo "Deployment: ${env.PROJECT_NAME_WITH_DASH}"
                    }
                }
            }
        }
        
        stage('Retrieve Image Tag') {
            steps {
                script {
                    // Get latest successful build number from build job
                    def buildJob = Jenkins.instance.getItem(env.BUILD_PROJECT_NAME)
                    def lastSuccessfulBuild = buildJob.getLastSuccessfulBuild()
                    env.IMAGE_TAG = lastSuccessfulBuild.getNumber().toString()
                    
                    echo "Deploying image tag: ${env.IMAGE_TAG}"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    if (params.DEPLOYMENT_TYPE == 'kubernetes') {
                        echo "Deploying to Kubernetes..."
                        sh """
                            export IMAGE_TAG=${env.IMAGE_TAG}
                            bash deploy_kube.sh
                        """
                    } else {
                        echo "Deploying with Docker Compose..."
                        sh """
                            export DOCKER_IMAGE_TAG=${env.IMAGE_TAG}
                            docker-compose down || true
                            docker-compose up -d
                        """
                    }
                    echo '✅ Deployment successful!'
                }
            }
        }
        
        stage('Sentry Release') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'sentry-auth-token', variable: 'SENTRY_AUTH_TOKEN')]) {
                        def gitCommit = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                        sh """
                            curl -sX POST https://sentry.io/api/0/organizations/${env.SENTRY_ORG}/releases/ \\
                                -H "Authorization: Bearer \$SENTRY_AUTH_TOKEN" \\
                                -H "Content-Type: application/json" \\
                                -d '{
                                    "version": "${gitCommit}",
                                    "projects": ["${env.SENTRY_PROJECT}"]
                                }' || echo "Sentry release creation failed (non-critical)"
                        """
                    }
                }
            }
        }
    }
}
```

---

## Checklist for New Projects

### 1. Environment Setup
- [ ] Create `.env` file with all configuration
- [ ] Add `.env` to `.gitignore`
- [ ] Create `env.example` template
- [ ] Upload `.env` to Jenkins credentials

### 2. Docker Configuration
- [ ] Update `docker-compose.yml` with env variables
- [ ] Update `Dockerfile` if needed
- [ ] Test Docker build locally

### 3. Deployment Scripts
- [ ] Update `deploy_kube.sh` with variable loading
- [ ] Add validation for required variables
- [ ] Test deployment script locally

### 4. Jenkins Pipeline
- [ ] Update `Jenkinsfile-build` with:
  - [ ] Jenkins API for .env creation
  - [ ] Variable parsing with null-safety
  - [ ] Derived variable computation
  - [ ] Remove hardcoded values
- [ ] Update `Jenkinsfile-deploy` similarly
- [ ] Test in Jenkins (might need 2-3 builds to debug)

### 5. Variables to Centralize
- [ ] Docker registry configuration (DOCKER_REGISTRY, DOCKER_REPOSITORY, etc.)
- [ ] Project names (ENV_PROJECT_NAME, BUILD_PROJECT_NAME)
- [ ] Deployment configuration (SERVER_NAME, DOCKER_PORT)
- [ ] Database URLs (DATABASE_URL, REDIS_CLOUD_URL)
- [ ] API keys (OAuth, Mailjet, Sentry, etc.)
- [ ] Storage configuration (AWS_*, MinIO)

### 6. Variables to Derive (Don't Store)
- [ ] BUILD_PROJECT_NAME → `${ENV_PROJECT_NAME}_build`
- [ ] PROJECT_NAME_WITH_DASH → `${ENV_PROJECT_NAME}` with underscores replaced
- [ ] NGINX_CONF_PATH → `/etc/nginx/sites-available/${PROJECT_NAME_WITH_DASH}`
- [ ] REGISTRY → `${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}`
- [ ] REPOSITORY → `${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${DOCKER_IMAGE_NAME}`

---

## Common Issues and Solutions

### Issue 1: Permission Denied Creating .env
**Symptom**: `/var/lib/jenkins/workspace/project@2@tmp/durable-xxx/script.sh.copy: 1: cannot create .env: Permission denied`

**Solution**: Use Jenkins APIs instead of shell commands:
```groovy
def envContent = readFile(file: env.ENV_FILE)
writeFile(file: '.env', text: envContent)
```

### Issue 2: ArrayIndexOutOfBoundsException
**Symptom**: `ArrayIndexOutOfBoundsException: Index 1 out of bounds for length 1`

**Solution**: Add null-safety check when parsing .env:
```groovy
def parts = envVar.split('=', 2)
def key = parts[0]
def value = parts.length > 1 ? parts[1] : ''  // Safe check
```

### Issue 3: Variables Show as "null"
**Symptom**: Docker image name shows as `null/null/null:123`

**Solution**: Don't reference variables in `environment{}` block. Load them in stages after .env is created.

### Issue 4: Changes Not Reflected in Build
**Symptom**: Jenkins build doesn't use latest code

**Solution**: 
```bash
git add .
git commit -m "Update Jenkins configuration"
git push
```
Jenkins pulls from remote repository, not local files.

---

## Benefits of This Approach

### ✅ Security
- Sensitive data in Jenkins credentials, not in code
- Single place to update secrets
- No accidental commits of credentials

### ✅ Maintainability
- One `.env` file instead of scattered configs
- Derived variables reduce duplication
- Easy to add new projects

### ✅ Reliability
- Jenkins native APIs work across all workspace types
- Null-safe parsing handles edge cases
- Fail-fast validation catches errors early

### ✅ Flexibility
- Easy to switch between environments (dev/staging/prod)
- Same pattern works for all projects
- Simple to add new environment variables

---

## Example: Applying to New Project "my_api"

1. **Create .env**:
```bash
ENV_PROJECT_NAME=my_api
DOCKER_REGISTRY=harbor.mycompany.com
DOCKER_REPOSITORY=library
DOCKER_IMAGE_NAME=my_api
DOCKER_IMAGE_TAG=latest
SERVER_NAME=api.mycompany.com
DOCKER_PORT=8080
```

2. **Derived Variables** (in Jenkinsfile):
```groovy
env.BUILD_PROJECT_NAME = "my_api_build"  // ${ENV_PROJECT_NAME}_build
env.PROJECT_NAME_WITH_DASH = "my-api"    // Replace _ with -
env.NGINX_CONF_PATH = "/etc/nginx/sites-available/my-api"
```

3. **Upload to Jenkins**:
- Credentials → Add → Secret file → ID: `my_api_env_file`

4. **Update Jenkinsfiles**:
- Change `credentialsId: 'my_api_env_file'`
- Follow templates above

5. **Test**:
- Push to GitHub
- Jenkins auto-triggers build
- Monitor console output

---

## Troubleshooting Commands

```bash
# Check Jenkins workspace permissions
ls -la /var/lib/jenkins/workspace/

# View .env file in Jenkins (add to Setup Environment stage)
sh "cat .env"

# Debug environment variables
sh "env | sort"

# Test Docker build locally
docker build -t test:latest .

# Test variable substitution in docker-compose
docker-compose config

# Validate .env parsing
cat .env | grep -v "^#" | grep -v "^$" | xargs
```

---

## References

- Jenkins Documentation: https://www.jenkins.io/doc/
- Docker Compose Environment Variables: https://docs.docker.com/compose/environment-variables/
- Groovy String Methods: https://groovy-lang.org/groovy-dev-kit.html

---

## Version History

- **v1.0** (2026-02-15): Initial guide based on arpansahu_dot_me project refactoring
  - Centralized Docker registry configuration
  - Fixed Jenkins permission errors with native APIs
  - Reduced .env variables by 57% through derivation
  - Added null-safe parsing and validation

---

*This guide is maintained as part of the arpansahu_dot_me project. Update this document when patterns evolve.*
