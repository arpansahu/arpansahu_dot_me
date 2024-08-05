#!/bin/bash

# Function to set up the environment
setup_environment() {
    # Path to the GIT_ASKPASS helper script
    GIT_ASKPASS_HELPER="$(pwd)/git-askpass.sh"

    # Create the GIT_ASKPASS helper script
    echo "Creating GIT_ASKPASS helper script"
    cat <<EOF > "$GIT_ASKPASS_HELPER"
#!/bin/sh
echo \$GIT_PASSWORD
EOF
    chmod +x "$GIT_ASKPASS_HELPER"

    # Export GIT_ASKPASS
    export GIT_ASKPASS="$GIT_ASKPASS_HELPER"
}

# Directory where the script is located
SCRIPT_DIR=$(pwd)

# Function to update Home.md for each repository
merge_main_into_build() {
    local repo_url=$1
    local repo_name=$(basename -s .git "$repo_url")

    # Extract repository path from URL
    REPO_PATH="${repo_url#https://github.com/}"

    # Construct the authenticated URL for prod
    AUTHENTICATED_URL="https://${GIT_USERNAME}@github.com/${REPO_PATH}"
   
    # Log the URL being used (without exposing the password)
    echo "Using URL: $AUTHENTICATED_URL"

    # Clone the repository
    echo "Cloning repository: $AUTHENTICATED_URL"
    if git clone "$AUTHENTICATED_URL"; then
        echo "Successfully cloned repository: $repo_url"
    else
        echo "Failed to clone repository: $repo_url"
        return 1
    fi

    # Navigate to the repository directory
    cd "$repo_name" || { echo "Failed to navigate to repository directory: $repo_name"; return 1; }
    
    # Check if the build branch exists and merge main into build
    if git rev-parse --verify build > /dev/null 2>&1; then
        git checkout build
        git rebase origin/main
        git push
    else
        echo "Branch 'build' does not exist in repository: $repo_url"
    fi
    
    # Navigate back to the script directory
    cd "$SCRIPT_DIR"

    # Remove the cloned repository
    echo "Cleaning up ..."
    rm -rf "playground_dir"
}

# Main script execution
main() {
    # This script is built for prod only
    # Setup the environment
    setup_environment
    mkdir "playground_dir"
    cd "playground_dir"
    merge_main_into_build "https://github.com/arpansahu/arpansahu_dot_me"
}

# Execute the main function with provided arguments or default to prod environment and all repositories
main "$@"