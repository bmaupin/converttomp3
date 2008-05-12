#!/usr/bin/python
import os, sys, shutil, subprocess
import ConvertToMP3

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

def ensureConversion(srcDir, destDir, srcType, destType):
	(srcFiles, expectedDestFiles) = getSrcAndExpectedDestFiles(srcDir, destDir, srcType, destType)
	destFiles = ConvertToMP3.getFilesEnding(destDir, destType)
	for file in expectedDestFiles:
		if file not in destFiles:
			return False
	return True

def main():
	srcDir1 = u"/home/bnsmith/download/playing/converttomp3_testing/El Ma\xf1ana Test Root"
	destDir1 = u"/home/bnsmith/download/playing/converttomp3_test_results"
	if os.path.isdir(destDir1):
	   shutil.rmtree(destDir1)
	subprocess.check_call([u"python", u"ConvertToMP3.py", srcDir1, destDir1])
	converted = ensureConversion(srcDir1, destDir1, u".m4a", u".mp3")
	if converted == True:
		print "Test succeeded!"
	else:
		print "Test failed!"

if __name__ == '__main__':
	main()