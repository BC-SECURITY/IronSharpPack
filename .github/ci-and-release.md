# CI Processes
## Update IronSharpPack .py files and Create PR (update_files.yml)
This workflow is manually triggered to update Python files based on executables from the SharpCollection repository. It processes these files, commits any changes, and creates a new branch and pull request into main.

Key Steps:
1. Process Executables: Runs a Python script to generate Python files from .NET executables across different .NET Framework versions.
2. Remove Unused Files: Cleans up any temporary or unnecessary files created during the run.
3. Create New Branch and Handle Changes: Checks for changes and commits them to a new branch, pushing the branch and creating a pull request if changes exist.


## Update Development Branch and PR to Main (release.yml)
This workflow is triggered manually via workflow_dispatch with an option to specify the type of version bump (patch, minor, or major). It's designed to increment the project version based on the latest entry in CHANGELOG.md, update the changelog, commit these changes to the dev branch, and then create a pull request to merge these changes into the main branch.

Key Steps:
1. Extract and Increment Version: It reads the current version from CHANGELOG.md, increments it based on the selected bump type, and then updates the environment variable for subsequent steps.
2. Update Changelog: Utilizes a community action to append the new version to CHANGELOG.md.
3. Commit Changes and Create Pull Request: Commits the updated changelog to dev and creates a pull request to merge dev into main.

## Create Release and Attach Files (tag_release.yml)
Triggered when a pull request to the main branch is closed and merged. It packages specified directories into ZIP files, creates a GitHub release tagged with the version number extracted from CHANGELOG.md, and uploads the ZIP files as assets to the release.

Key Steps:
1. Determine New Version: Parses CHANGELOG.md to find the latest version number.
2. Zip NetFramework folders: Compresses folders containing different versions of .NET Framework files into ZIP files.
3. Create Release and Upload Release Asset: Creates a new GitHub release with the specified version and uploads the previously zipped files as release assets.
