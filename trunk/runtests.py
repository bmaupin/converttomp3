#!/usr/bin/python
#
#    Copyright (C) Brad Smith 2008
#
#    This file is part of ConvertToMP3
#
#    ConvertToMP3 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ConvertToMP3 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ConvertToMP3.  If not, see <http://www.gnu.org/licenses/>.

import os, shutil, subprocess
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3

import ConvertToMP3

testerrors = []

def uncommonPostfix(file1, file2):
    commonPrefix = os.path.commonprefix([file1, file2])
    longerStr = file1
    if len(file1) < len(file2):
        longerStr = file2
    return longerStr[len(commonPrefix):]

def getSrcAndExpectedDestFiles(srcDir, destDir, srcEnding, destEnding):
    srcFiles = []
    expectedDestFiles = []
    for current, _, files in os.walk(srcDir, True):
        for f in files:
            if f.lower().endswith(srcEnding):
                srcFile = os.path.join(srcDir, current, f)
                srcFiles.append(srcFile)
                srcFileName = os.path.split(srcFile)[1]
                srcFileNoExt = srcFileName[:-(len(srcEnding))]
                relativePath = uncommonPostfix(srcDir, current)
                destFile = os.path.join(os.path.normpath(destDir + relativePath
                                        ), srcFileNoExt + destEnding)
                expectedDestFiles.append(destFile)
    return (srcFiles, expectedDestFiles)

def tagEqual(srcFile, destFile, tagType):
    tagNameMap = {"title": ('\xa9nam', 'TIT2'),
                  "artist": ('\xa9ART', 'TPE1'),
                  "album": ('\xa9alb', 'TALB'),
                  "track": ('trkn', 'TRCK'),
                  "genre": ('\xa9gen', 'TCON'),
                  "group": ('\xa9grp', 'TIT1')}
    assert srcFile[-4:].lower() == '.m4a'
    srcTagInfo = MP4(srcFile)
    assert destFile[-4:].lower() == '.mp3'
    destTagInfo = MP3(destFile)

    srcTagName = tagNameMap[tagType][0]
    destTagName = tagNameMap[tagType][1]
    if srcTagInfo.tags.has_key(srcTagName) == False \
                and destTagInfo.tags.has_key(destTagName) == False:
        return True
    if srcTagInfo.tags.has_key(srcTagName) == True \
                and destTagInfo.tags.has_key(destTagName) == False:
        return False

    srcTag = srcTagInfo.tags[srcTagName]
    while type(srcTag) == list or type(srcTag) == tuple:
        srcTag = srcTag[0]
    if type(srcTag) == int:
        srcTag = str(srcTag)
    srcTagStr = srcTag.encode('UTF-8')
    destTagStr = unicode(destTagInfo.tags[destTagName]).encode('UTF-8')
    if srcTagStr != destTagStr:
        testerrors.append('Conversion failed: ' + tagType +
                          ' did not match: ' + srcTagStr + ' ' + destTagStr)
        return False
    return True

def checkTags(srcFile, destFile):
    for tagType in ['title', 'artist', 'album', 'track', 'genre', 'group']:
        if tagEqual(srcFile, destFile, tagType) == False:
            return False
    return True

def ensureConversion(srcDir, destDir, srcType, destType):
    (srcFiles, expectedDestFiles) = getSrcAndExpectedDestFiles(srcDir, destDir,
                                                            srcType, destType)
    destFiles = ConvertToMP3.getFilesEnding(destDir, destType)
    for f in expectedDestFiles:
        if f not in destFiles:
            testerrors.append('Conversion failed: ' + f + ' was not found.')
            return False
    for (src, dest) in zip(srcFiles, expectedDestFiles):
        if checkTags(src, dest) == False:
            testerrors.append('Conversion failed: ' + dest +
                              ' had incorrect tags.')
            return False
    return True

def main():
    results = []

    srcDir1 = u"/home/bnsmith/download/playing/converttomp3_testing/" \
              u"El Ma\xf1ana Test Root"
    destDir1 = u"/home/bnsmith/download/playing/converttomp3_test_results/" \
               u"El Ma\xf1ana Test Results"
    if os.path.isdir(destDir1):
        shutil.rmtree(destDir1)
    subprocess.check_call([u"python", u"ConvertToMP3.py", srcDir1, destDir1])
    results.append(ensureConversion(srcDir1, destDir1, u".m4a", u".mp3"))

    srcDir2 = u"/home/bnsmith/download/playing/converttomp3_testing/" \
              u"WONKY-FILES_ROOT"
    destDir2 = u"/home/bnsmith/download/playing/converttomp3_test_results/" \
              u"WONKY-FILES_ROOT_RESULTS"
    if os.path.isdir(destDir2):
        shutil.rmtree(destDir2)
    subprocess.check_call([u"python", u"ConvertToMP3.py", srcDir2, destDir2])
    results.append(ensureConversion(srcDir2, destDir2, u".m4a", u".mp3"))

    allSucceeded = True
    for res in results:
        if res == False:
            allSucceeded = False

    print "\n***********************************************************"
    if allSucceeded == True:
        print "Tests succeeded!"
    else:
        print "Tests failed!"
    print "***********************************************************"

    for err in testerrors:
        print err

if __name__ == '__main__':
    main()