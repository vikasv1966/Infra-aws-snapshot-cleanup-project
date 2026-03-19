#!/bin/bash

set -e

echo "Packaging lambda..."

# clean old zip if exists
rm -f lambda.zip

# go to src directory
cd ../src/snapshot_cleanup

# create zip
zip -r ../../lambda.zip .

cd -

echo "Package created: lambda.zip"