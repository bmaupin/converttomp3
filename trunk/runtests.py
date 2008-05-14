#!/usr/bin/python
import os, sys, shutil, subprocess
from mutagen.mp4 import MP4, MP4StreamInfoError
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
	for current, dirs, files in os.walk(srcDir, True):
		for f in files:
			if f.lower().endswith(srcEnding):
				srcFile = os.path.join(srcDir, current, f)
				srcFiles.append(srcFile)
				srcFileName = os.path.split(srcFile)[1]
				srcFileNoExt = srcFileName[:-(len(srcEnding))]
				relativePath = uncommonPostfix(srcDir, current)
				destFile = os.path.join(os.path.normpath(destDir + relativePath), srcFileNoExt + destEnding)
				expectedDestFiles.append(destFile)
	return (srcFiles, expectedDestFiles)

def tagEqual(srcFile, destFile, tagType):
	tagNameMap = {"title": ('\xa9nam', 'TIT2'),
				  "artist": ('\xa9ART', 'TPE1'),
				  "album": ('\xa9alb', 'TALB'),
				  "track": ('trkn', 'TRCK'),
				  "genre": ('\xa9gen', 'TCON')}
	assert srcFile[-4:].lower() == '.m4a'
	srcTagInfo = MP4(srcFile)
	assert destFile[-4:].lower() == '.mp3'
	destTagInfo = MP3(destFile)
	
	# Not sure what's going on with encodings here. It seems like the M4A library
	# returns unicode strings with the latin-1 encoding, so calling 'encode' with 'UTF-8' returns
	# a byte string that is unchanged and still in latin-1. When the MP3 library has its tag
	# object cast to a unicode string, it seems to be encoded in UTF-8, and so needs to be
	# encoded as latin-1 to be compared with the M4A string. WTF?
	srcTagName = tagNameMap[tagType][0]
	srcTag = srcTagInfo.tags[srcTagName]
	while type(srcTag) == list or type(srcTag) == tuple:
		srcTag = srcTag[0]
	if type(srcTag) == int:
		srcTag = str(srcTag)
	srcTagStr = srcTag.encode('UTF-8')
	destTagName = tagNameMap[tagType][1]
	destTagStr = unicode(destTagInfo.tags[destTagName]).encode('latin-1')
	if srcTagInfo.tags.has_key(srcTagName) and srcTagStr != destTagStr:
		testerrors.append('Conversion failed: ' + tagType + ' did not match: ' + srcTagStr + ' ' + destTagStr)
		return False
	return True

def checkTags(srcFile, destFile):
	for tagType in ['title', 'artist', 'album', 'track', 'genre']:
		if tagEqual(srcFile, destFile, tagType) == False:
			return False
	return True

def ensureConversion(srcDir, destDir, srcType, destType):
	(srcFiles, expectedDestFiles) = getSrcAndExpectedDestFiles(srcDir, destDir, srcType, destType)
	destFiles = ConvertToMP3.getFilesEnding(destDir, destType)
	for file in expectedDestFiles:
		if file not in destFiles:
			testerrors.append('Conversion failed: ' + file + ' was not found.')
			return False
	for (src, dest) in zip(srcFiles, expectedDestFiles):
		if checkTags(src, dest) == False:
			testerrors.append('Conversion failed: ' + dest + ' had incorrect tags.')
			return False
	return True

def main():
	srcDir1 = u"/home/bnsmith/download/playing/converttomp3_testing/El Ma\xf1ana Test Root"
	destDir1 = u"/home/bnsmith/download/playing/converttomp3_test_results/El Ma\xf1ana Test Results"
	if os.path.isdir(destDir1):
	   shutil.rmtree(destDir1)
	subprocess.check_call([u"python", u"ConvertToMP3.py", srcDir1, destDir1])
	test1 = ensureConversion(srcDir1, destDir1, u".m4a", u".mp3")
	
	print "\n**************************************************************************"
	if test1 == True:
		print ("Test succeeded!").encode('UTF-8')
	else:
		print ("Test failed!").encode('UTF-8')
	print "**************************************************************************"
	
	for err in testerrors:
		print err.encode('UTF-8')

if __name__ == '__main__':
	main()