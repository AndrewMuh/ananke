#!/bin/bash
#
# Automated release workflow script for the Ananke package
# Requires a configuration file with format "username password"

VERSION_TYPE=$1
CONFIG=pypi_login.txt
DEV=dev
MASTER=master

if [[ -n $(git status -s) ]];
then
    echo "Unstaged/uncommitted changes; aborting"
    exit 1
fi


if [ ! -f "$CONFIG" ]; then
    echo "Configuration file does not exist"
    exit 1
fi

git fetch --all
git checkout $DEV 
git merge $MASTER --no-edit

poetry version $VERSION_TYPE

VERSION="$(poetry version -s)"
echo $VERSION
parse-changelog --changelog CHANGELOG.md --release $VERSION
pre-commit run --all-files
git commit -am "$VERSION"
git tag -a v$VERSION -m "v$VERSION"
git checkout $MASTER 
git merge $DEV --no-edit
poetry build
git push origin --tags
git push origin dev
git push origin master
USERNAME=$(awk '{print $1}' $CONFIG)
PASSWORD=$(awk '{print $2}' $CONFIG)
poetry publish --username $USERNAME --password $PASSWORD
git checkout $DEV
