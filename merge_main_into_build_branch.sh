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

    # Fetch all branches from the remote
    git fetch origin

    # Check if the build branch exists in the remote repository and merge main into build
    if git show-ref --verify --quiet "refs/remotes/origin/build"; then
        git checkout build
        git rebase origin/main
        git push
    else
        echo "Branch 'build' does not exist in the remote repository: $repo_url"
    fi
    
    # Navigate back to the playground directory
    cd "$SCRIPT_DIR/playground_dir"

    # Remove the cloned repository
    echo "Cleaning up ..."
    rm -rf "$repo_name"
}

# Main script execution
main() {
    # This script is built for prod only
    # Setup the environment
    setup_environment
    mkdir "playground_dir"
    cd "playground_dir"
    merge_main_into_build "https://github.com/arpansahu/arpansahu_dot_me"

    # Navigate back to the script directory and clean up the playground directory
    cd "$SCRIPT_DIR"
    echo "Removing playground directory ..."
    rm -rf "playground_dir"
}

# Execute the main function with provided arguments or default to prod environment and all repositories
main "$@"