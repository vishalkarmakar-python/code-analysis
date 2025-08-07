# Git Setup and Integration Guide

This guide covers Git installation and essential commands for managing both local and remote repositories.

## Table of Contents

- [Git Installation](#git-installation)
  - [Windows Installation](#windows-installation)
  - [Initial Configuration](#initial-configuration)
  - [Authentication Setup](#authentication-setup)
- [Git Integration](#git-integration)
  - [Local Git Commands](#local-git-commands)
  - [Remote Git Commands](#remote-git-commands)
  - [Branch Synchronization](#branch-synchronization)
  - [Branch Workflow Strategies](#branch-workflow-strategies)
  - [Correction Branch Workflow](#correction-branch-workflow)

## Git Installation

### Windows Installation

1. **Download Git for Windows**

   - Visit the [Git for Windows](https://git-scm.com/download/win) website
   - Download the latest 64-bit Git for Windows installer

2. **Run the Installer**

   - Double-click the downloaded executable
   - Click "Next" to start the installation wizard

3. **Choose Components**

   - Keep the default selections
   - Optionally check "Windows Explorer integration" for right-click Git operations
   - Click "Next"

4. **Choose Default Editor**

   - Select your preferred editor (VS Code recommended if installed)
   - Click "Next"

5. **Adjust PATH Environment**

   - Select "Git from the command line and also from 3rd-party software"
   - Click "Next"

6. **Choose HTTPS Transport Backend**

   - Select "Use the OpenSSL library"
   - Click "Next"

7. **Configure Line Ending Conversions**

   - Select "Checkout Windows-style, commit Unix-style line endings"
   - Click "Next"

8. **Configure Terminal Emulator**

   - Select "Use Windows' default console window"
   - Click "Next"

9. **Configure Extra Options**

   - Enable "Enable file system caching" for performance
   - Enable "Enable Git Credential Manager" for easier authentication
   - Click "Next"

10. **Experimental Options**

    - Leave unchecked unless you need specific experimental features
    - Click "Install" to begin installation

11. **Complete Installation**
    - Wait for the installation to complete
    - Click "Finish"

### Initial Configuration

After installing Git, set up your identity:

```bash
# Set your username
git config --global user.name "Your Name"

# Set your email address
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Configure line endings (if needed)
git config --global core.autocrlf input
```

### Authentication Setup

#### HTTPS Authentication with Git Credential Manager

Git Credential Manager should be installed by default with Git for Windows. To ensure it's working:

```bash
# Verify credential helper is set up
git config --global credential.helper

# Should return "manager" or "manager-core"
# If not, set it manually:
git config --global credential.helper manager
```

#### SSH Authentication

1. **Generate SSH Key** (if you don't already have one):

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key to agent
ssh-add ~/.ssh/id_ed25519
```

2. **Add SSH Key to GitHub/GitLab/etc.**:

   - Copy the SSH public key:

     ```bash
     # For Windows PowerShell
     Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard

     # For Windows Command Prompt
     type %USERPROFILE%\.ssh\id_ed25519.pub | clip
     ```

   - Paste the key in your Git provider's SSH key settings

## Git Integration

This section covers essential Git commands for both local and remote repository management.

### Local Git Commands

| Category              | Operation                | Command                                              | Description                                        |
| --------------------- | ------------------------ | ---------------------------------------------------- | -------------------------------------------------- |
| **Setup**             | Initialize repository    | `git init`                                           | Create new Git repository                          |
|                       | Configure user name      | `git config --local user.name "Your Name"`           | Set username for current repository                |
|                       | Configure email          | `git config --local user.email "email@example.com"`  | Set email for current repository                   |
|                       | Configure global name    | `git config --global user.name "Your Name"`          | Set default username for all repositories          |
|                       | Configure global email   | `git config --global user.email "email@example.com"` | Set default email for all repositories             |
| **Basic Actions**     | Add file                 | `git add <file_name>`                                | Add specific file into Staging                     |
|                       | Remove file              | `git rm --cached <file_name>`                        | Remove specific file from Staging                  |
|                       | Add all files            | `git add .`                                          | Stage all changes                                  |
|                       | Add by pattern           | `git add *.py`                                       | Stage files by pattern                             |
|                       | Commit changes           | `git commit -m "<Commit Message>"`                   | Record changes to repository                       |
|                       | Commit with details      | `git commit -m "<Title>" -m "<Description>"`         | Add detailed commit message                        |
|                       | Amend commit             | `git commit --amend`                                 | Modify the most recent commit                      |
|                       | Amend without edit       | `git commit --amend --no-edit`                       | Add changes to last commit without editing message |
| **Information**       | Check status             | `git status`                                         | View working tree status                           |
|                       | Show commit details      | `git show <commit_id>`                               | Display specific commit details                    |
|                       | Show raw details         | `git show <commit_id> --raw`                         | Display file changes in commit                     |
|                       | View history             | `git log`                                            | Show commit history                                |
|                       | View compact history     | `git log --oneline`                                  | Show compact commit history                        |
|                       | View branch history      | `git log --graph --oneline --all`                    | Display visual history with branches               |
|                       | List branches            | `git branch`                                         | Show local branches                                |
|                       | Show latest commit       | `git show`                                           | Display most recent commit                         |
|                       | View changes             | `git diff`                                           | Show unstaged changes                              |
|                       | View staged changes      | `git diff --staged`                                  | Show changes that will be committed                |
|                       | View file history        | `git log -p <file_name>`                             | Show commits that changed a file                   |
|                       | Find commits by text     | `git log -S "<text>"`                                | Find commits containing specific text              |
|                       | Compare branches         | `git diff main..develop`                             | Compare differences between main and develop       |
|                       | Find branch divergence   | `git log main..develop`                              | Show commits in develop that aren't in main        |
| **Branch Management** | Create branch            | `git branch <branch_name>`                           | Create new branch                                  |
|                       | Switch branch            | `git checkout <branch_name>`                         | Switch to existing branch                          |
|                       | Create and Switch branch | `git checkout -b <branch_name>`                      | Create and switch to new branch                    |
|                       | Rename branch            | `git branch -m <old_name> <new_name>`                | Rename a branch                                    |
|                       | Merge branch             | `git merge <branch_name>`                            | Merge changes from branch                          |
|                       | Abort merge              | `git merge --abort`                                  | Abort an in-progress merge                         |
|                       | Delete branch            | `git branch -d <branch_name>`                        | Remove branch (safe)                               |
|                       | Force delete branch      | `git branch -D <branch_name>`                        | Remove branch regardless of status                 |
|                       | Create feature branch    | `git checkout -b feature/<name>`                     | Create a new feature branch                        |
|                       | Create bugfix branch     | `git checkout -b bugfix/<name>`                      | Create a bugfix branch                             |
|                       | Create release branch    | `git checkout -b release/<version>`                  | Create a release branch                            |
|                       | Create correction branch | `git checkout -b correction/<name>`                  | Create a branch for code corrections               |
|                       | Merge develop to main    | `git checkout main && git merge develop`             | Update main with development changes               |
|                       | Merge feature to develop | `git checkout develop && git merge feature/<name>`   | Integrate feature into development branch          |
|                       | Cherry-pick to main      | `git checkout main && git cherry-pick <commit_id>`   | Apply specific fixes to production branch          |
|                       | Tag release              | `git tag -a v1.0.0 -m "Release v1.0.0"`              | Create annotated tag for release                   |
| **Temporary Storage** | Stash changes            | `git stash`                                          | Save changes temporarily                           |
|                       | Stash with message       | `git stash save "<message>"`                         | Save changes with descriptive message              |
|                       | List stashes             | `git stash list`                                     | Show all stashed changes                           |
|                       | Apply stashed changes    | `git stash apply`                                    | Restore most recent stashed changes                |
|                       | Apply specific stash     | `git stash apply stash@{n}`                          | Restore specific stash                             |
|                       | Pop stash                | `git stash pop`                                      | Apply and remove stash                             |
|                       | Remove stash             | `git stash drop stash@{n}`                           | Delete a specific stash                            |
|                       | Clear all stashes        | `git stash clear`                                    | Remove all stashed changes                         |
|                       | Stash before switching   | `git stash && git checkout main`                     | Quick save before changing branches                |
| **Undo Operations**   | Discard file changes     | `git checkout -- <file_name>`                        | Revert changes to file                             |
|                       | Unstage file             | `git restore --staged <file_name>`                   | Remove file from staging area                      |
|                       | Reset to commit          | `git reset <commit_id>`                              | Move branch pointer to specific commit             |
|                       | Hard reset               | `git reset --hard <commit_id>`                       | Reset pointer and discard all changes              |
|                       | Soft reset               | `git reset --soft <commit_id>`                       | Reset pointer but keep staged changes              |
|                       | Revert commit            | `git revert <commit_id>`                             | Create new commit that undoes changes              |
|                       | Revert merge commit      | `git revert -m 1 <merge_commit_id>`                  | Revert a merge commit in production                |

### Remote Git Commands

| Category                | Operation                | Command                                                  | Description                                   |
| ----------------------- | ------------------------ | -------------------------------------------------------- | --------------------------------------------- |
| **Remote Setup**        | Clone repository         | `git clone <repository_url>`                             | Copy remote repository locally                |
|                         | Clone specific branch    | `git clone -b <branch> <repository_url>`                 | Clone only a specific branch                  |
|                         | Clone shallow            | `git clone --depth=1 <repository_url>`                   | Clone with limited history                    |
|                         | Add remote               | `git remote add <name> <repository_url>`                 | Add remote repository reference               |
|                         | Add upstream             | `git remote add upstream <original_repo_url>`            | Add original repo as upstream                 |
|                         | Show remote info         | `git remote -v`                                          | List remote connections                       |
|                         | Show remote repository   | `git remote -v show`                                     | List all remote connections                   |
|                         | Change remote URL        | `git remote set-url <name> <new_url>`                    | Update remote repository URL                  |
|                         | Rename remote            | `git remote rename <old_name> <new_name>`                | Change remote reference name                  |
|                         | Remove remote            | `git remote remove <name>`                               | Delete remote connection                      |
| **Synchronizing**       | Fetch changes            | `git fetch <remote>`                                     | Download objects from remote                  |
|                         | Fetch all remotes        | `git fetch --all`                                        | Download from all remotes                     |
|                         | Fetch prune              | `git fetch --prune`                                      | Fetch and remove deleted remote branches      |
|                         | Pull changes             | `git pull <remote> <branch>`                             | Fetch and merge remote changes                |
|                         | Pull with rebase         | `git pull --rebase <remote> <branch>`                    | Pull and reapply local commits                |
|                         | Push changes             | `git push <remote> <branch>`                             | Upload local commits to remote                |
|                         | Push all branches        | `git push --all <remote>`                                | Push all local branches                       |
|                         | Force push               | `git push --force <remote> <branch>`                     | Overwrite remote branch (use with caution)    |
|                         | Push tags                | `git push --tags <remote>`                               | Push all tags to remote                       |
|                         | Update develop from main | `git checkout develop && git merge origin/main`          | Sync development branch with production       |
|                         | Update main from develop | `git checkout main && git merge origin/develop`          | Push development changes to production        |
|                         | Force push feature       | `git push --force-with-lease origin feature/<name>`      | Safer force push after rebasing               |
|                         | Update all branches      | `git pull --all`                                         | Fetch and merge all tracked branches          |
| **Branch Management**   | List remote branches     | `git branch -r`                                          | Show remote branches                          |
|                         | List all branches        | `git branch -a`                                          | Show local and remote branches                |
|                         | Track remote branch      | `git checkout --track <remote>/<branch>`                 | Create local branch tracking remote           |
|                         | Set upstream             | `git push --set-upstream <remote> <branch>`              | Push and track branch                         |
|                         | Push and track           | `git push -u origin <branch>`                            | Shorter form of set-upstream                  |
|                         | Push correction branch   | `git push -u origin correction/<name>`                   | Push and track correction branch              |
|                         | Delete remote branch     | `git push origin --delete <branch>`                      | Remove branch from remote                     |
|                         | Delete remote branch alt | `git push <remote> :<branch>`                            | Alternative syntax for deletion               |
|                         | Set default branch       | `git remote set-head origin -a`                          | Auto-detect default branch                    |
|                         | Create remote branch     | `git push origin local-branch:remote-branch`             | Create branch with different name on remote   |
|                         | Reset to remote          | `git reset --hard origin/main`                           | Reset local branch to match remote            |
|                         | Get latest release       | `git fetch --tags && git checkout $(git tag \| tail -1)` | Checkout the most recent tag                  |
| **Advanced Operations** | Update forked repo       | `git fetch upstream` + `git merge upstream/main`         | Sync fork with original repository            |
|                         | Compare branches         | `git diff <branch1>..<branch2>`                          | Show differences between branches             |
|                         | Show remote branches     | `git remote show <remote>`                               | Detailed info about remote                    |
|                         | Clean untracked files    | `git clean -fd`                                          | Remove untracked files and directories        |
|                         | Show remote log          | `git log <remote>/<branch>`                              | View commit history of remote branch          |
|                         | Merge remote branch      | `git merge <remote>/<branch>`                            | Merge remote branch into current branch       |
|                         | Cherry-pick commit       | `git cherry-pick <commit_id>`                            | Apply changes from specific commit            |
|                         | Push specific tag        | `git push <remote> <tag_name>`                           | Push single tag to remote                     |
|                         | Rename branches remotely | `git push origin :old-name new-name`                     | Delete old and push new branch in one command |
|                         | Remote prune ref         | `git remote prune origin`                                | Delete tracking branches that no longer exist |
|                         | Push new default branch  | `git push -u origin main`                                | Push and set new default branch               |
|                         | Protect branches         | _Web UI setting in GitHub/GitLab_                        | Configure branch protection in remote repo    |

### Branch Synchronization

This section covers strategies and commands for synchronizing branches between local and remote repositories, ensuring consistent state across environments.

#### Synchronizing After Local Merges

When you've merged branches locally (e.g., merged develop into main), you need to synchronize these changes with remote repositories:

```bash
# Check current branches and their status
git branch -vv

# Scenario: You've merged develop into main locally and need to sync
# First, ensure local main has the merged changes
git checkout main

# Push the updated main branch to remote
git push origin main

# Now sync the develop branch with any changes
git checkout develop
git pull origin develop  # Get any remote changes first
git push origin develop  # Push any local changes
```

#### Synchronizing After Remote Changes

When changes have been made in the remote repository (e.g., through a Pull Request on GitHub), you need to sync your local branches:

```bash
# Update your local tracking information
git fetch --all --prune

# Update local main branch
git checkout main
git pull origin main

# Update local develop branch
git checkout develop
git pull origin develop
```

#### Complete Branch Synchronization

For a full synchronization of both local and remote branches after significant changes:

```bash
# Get latest from all remotes
git fetch --all --prune

# Synchronize main branch
git checkout main
git pull origin main  # Update local main from remote
git push origin main  # Ensure remote is up to date

# Synchronize develop branch
git checkout develop
git pull origin develop  # Update local develop from remote
git push origin develop  # Ensure remote is up to date
```

#### Handling Deleted Projects or Files

If you've deleted projects or files in one branch and need to propagate these deletions:

```bash
# If you deleted files in develop and merged to main
git checkout main
git merge develop
git push origin main

# To ensure develop is also in sync after changes in main
git checkout develop
git merge main
git push origin develop
```

#### Synchronization After Conflict Resolution

If you encounter merge conflicts during synchronization:

```bash
# During a merge with conflicts
git status  # Check which files have conflicts
# Resolve conflicts in your editor
git add .  # Add resolved files
git commit -m "Resolve merge conflicts between main and develop"

# Push the resolved merge to remote
git push origin main

# Sync other branches
git checkout develop
git merge main  # To ensure develop has conflict resolutions
git push origin develop
```

#### Quick Sync Commands Reference

Common commands for maintaining branch synchronization:

| Scenario                    | Command Sequence                                                                                                 |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Sync after local merge      | `git checkout main && git push origin main && git checkout develop && git merge main && git push origin develop` |
| Sync after remote changes   | `git fetch --all && git checkout main && git pull && git checkout develop && git pull`                           |
| Propagate deletions         | `git checkout main && git merge develop && git push origin main`                                                 |
| Reset local to match remote | `git fetch origin && git reset --hard origin/main`                                                               |
| Force remote to match local | `git push --force origin main` (use with caution)                                                                |
| Verify sync status          | `git fetch --all && git branch -vv`                                                                              |

### Branch Workflow Strategies

This section describes common branching strategies for managing development and production code.

#### Git Flow Workflow

A robust branching strategy with dedicated branches for features, releases, and hotfixes.

**Main Branches:**

- `main` - Production-ready code, always stable
- `develop` - Integration branch for features, pre-production

**Supporting Branches:**

- `feature/*` - New features, branched from and merged back to `develop`
- `release/*` - Preparation for release, branched from `develop`, merged to both `develop` and `main`
- `hotfix/*` - Production fixes, branched from `main`, merged to both `develop` and `main`
- `correction/*` - Code corrections and improvements, typically branched from `main` or `develop`

**Common Commands:**

```bash
# Feature development
git checkout develop
git checkout -b feature/new-feature
# Work on feature...
git checkout develop
git merge feature/new-feature

# Release preparation
git checkout develop
git checkout -b release/1.0.0
# Final adjustments...
git checkout main
git merge release/1.0.0
git checkout develop
git merge release/1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"

# Hotfix
git checkout main
git checkout -b hotfix/critical-fix
# Fix the issue...
git checkout main
git merge hotfix/critical-fix
git checkout develop
git merge hotfix/critical-fix
git tag -a v1.0.1 -m "Version 1.0.1"
```

#### GitHub Flow

A simplified workflow centered around feature branches and pull requests.

**Main Branches:**

- `main` - Production-ready code

**Supporting Branches:**

- Feature branches - All development happens in feature branches

**Common Commands:**

```bash
# Start new work
git checkout main
git pull origin main
git checkout -b my-new-feature

# Submit for review (after pushing to GitHub, create PR through web UI)
git push -u origin my-new-feature

# After PR approval and merge on GitHub, clean up
git checkout main
git pull origin main
git branch -d my-new-feature
```

#### Correction Branch Workflow

A specialized workflow for making code corrections and improvements.

**Process:**

1. **Create a correction branch from the main branch**

   ```bash
   git checkout main
   git pull origin main
   git checkout -b correction/docstring-updates
   ```

2. **Make corrections and commit them**

   ```bash
   # Make your changes
   git add .
   git commit -m "Add comprehensive docstrings to improve code documentation"
   ```

3. **Push the branch to the remote repository and track it**

   ```bash
   git push -u origin correction/docstring-updates
   ```

4. **Create a Pull Request (if using GitHub/GitLab)**

   - Navigate to your repository on GitHub/GitLab
   - Click "Compare & pull request"
   - Add description of corrections
   - Submit the pull request

5. **Merge the correction branch into main (after review)**

   ```bash
   git checkout main
   git pull origin main  # Get any updates first
   git merge correction/docstring-updates
   git push origin main
   ```

6. **Clean up after merging**

   ```bash
   # Delete local branch
   git branch -d correction/docstring-updates

   # Delete remote branch
   git push origin --delete correction/docstring-updates
   ```

7. **Sync other branches with the corrections (if needed)**
   ```bash
   git checkout develop
   git pull origin develop  # Get latest changes
   git merge main           # Pull in corrections from main
   git push origin develop  # Update remote develop branch
   ```

#### Release & Production Management

Commands for handling synchronization between development and production:

```bash
# Update develop with production bugfixes
git checkout develop
git merge main

# Prepare release from develop
git checkout develop
git checkout -b release/v1.2.0
# Test and finalize release...

# Push release to production
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# Sync develop with the new release
git checkout develop
git merge main
```

#### Multiple Remote Repositories

This section explains how to work with multiple remote repositories for different environments.

**Common Structure:**

```
* develop           # Local development branch
  main              # Local production branch
  remotes/dev/develop  # Remote development environment
  remotes/dev/main
  remotes/prd/develop  # Remote production environment
  remotes/prd/main
```

**Setup Commands:**

```bash
# Create local branches
git checkout -b main    # If not already on main
git checkout -b develop # Create development branch

# Add multiple remote repositories
git remote add dev https://github.com/yourusername/project-dev.git
git remote add prd https://github.com/yourusername/project-prod.git

# Push branches to both remotes
git checkout main
git push dev main
git push prd main

git checkout develop
git push dev develop
git push prd develop

# Verify the structure
git branch -a
```

**Working with Multiple Remotes:**

```bash
# Pull from specific remote
git pull dev develop   # Get latest from development environment
git pull prd main      # Get latest from production environment

# Push to specific remote
git push dev develop   # Push to development environment
git push prd main      # Push to production environment

# Fetch from all remotes
git fetch --all

# See remote details
git remote show dev
git remote show prd
```

**Environment Synchronization:**

Commands for keeping development and production environments in sync:

```bash
# Update local branches from remotes
git checkout develop
git pull dev develop
git checkout main
git pull prd main

# Sync between environments (dev to prod)
git checkout main
git merge develop
git push prd main

# Sync production changes back to development
git checkout develop
git merge main
git push dev develop
```
