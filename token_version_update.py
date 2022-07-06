import re
import sys

kExactString = "exact"
kSearchURL = "https://github.com/yml-org/mayo-design-tokens-ios.git"
kFilename = "Package.swift"

def inplaceChange(filename, oldString, newString):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if oldString not in s:
            print('"{oldString}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print('Changing "{oldString}" to "{newString}" in {filename}'.format(**locals()))
        s = s.replace(oldString, newString)
        f.write(s)

# Replace new version with old version.
# filename: str. Name of the file to be updated in.
# curLine: str. Line containing current version.
# curVersion: str. Current version.
# newVersion: str. New version.
def writeVersion(filename, curLine, curVersion, newVersion):
    newLine = curLine.replace(curVersion, newVersion)
    inplaceChange(filename, curLine, newLine)

# Extract the version from the line.
# line: str. String containing the word exact with version.
# returns: str. Version, extracted from the line.
def captureVersion(line):
    # Extract after exact...
    return re.search('exact: "(.+?)"', line).group(1)

# Update the exact version of the url in the given file name with new version.
# filename: str. Name of the file to be updated in.
# searchURL: str. Dependency url for which version to be updated.
# newVersion: str. New version.
def updateExactVersion(filename, searchURL, newVersion):
    isSearchUrlFound = False
    
    with open(filename) as file:  
        # Read line by line...
        for line in file.readlines():

            if isSearchUrlFound:
                # URL was found, but exact was not found in the previous iteration. 
                # Search exact in the immediate next line. 
                if kExactString in line:
                    writeVersion(filename, line, captureVersion(line), newVersion)
                # break the loop here. Futher traversal is not required because the url doesn't contain 'exect'.
                break

            # Match search URL...
            if searchURL in line:
                isSearchUrlFound = True
                # Check if this line contains the word "exact"...
                if kExactString in line:
                    writeVersion(filename, line, captureVersion(line), newVersion)
                    break

# Validate if file recieves version as argument.
if len(sys.argv) == 1:
    print ('Required new version')
    sys.exit(-1)

# Invoke the method to update version.
updateExactVersion(kFilename, kSearchURL, sys.argv[1])
