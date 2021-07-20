# Generates Sonygan json for a collection of audio files

# Input: Audio/Sound files/Path
# Output: Examples.json in SonyGan format
# Fileformat: soundName--p1-val--p2-val--..--seg-val.wav

# Segment pop

import numpy as np
import os  # for mkdir
import sys
import json
import math
import pdb

class nsJson():
	def __init__(self, filePath, outPath, src, sr, soundSource):
		self.filePath = filePath
		self.outPath = outPath
		self.soundSource = soundSource
		if src == "natural" or src == 0:
			self.srcType_string = "Natural"
			self.srcType = 0  # dataset type: 0 or "natural" and 1 or "artificial".
		elif src == "generated" or src == 1:
			self.srcType_string = "Generated"
			self.srcType = 1  # dataset type: 0 or "natural" and 1 or "artificial".
		else:
			self.srcType_string = "Undecided"
			self.srcType = 2  # dataset type: 0 or "natural" and 1 or "artificial".
		self.sr = sr
		self.fileList =  []
		self.SGjson = {}
		self.readAll()

	def readOne(self):
		#Reads single Files and stores metaParams
		print("read single files")

	def readAll(self):
		# Reads all files in a folder
		fileList = [f for f in os.listdir(self.filePath) if '.wav' in f]
		self.fileList = fileList
		self.storeRecords()

	'''Stores records for all the files in the given directory'''
	def storeRecords(self):

		for filename in self.fileList:
		    sgrecord = {}
		    fileArr = os.path.splitext(filename)[0].split("--")
		    sgrecord["sound_name"] = filename

		    # for x in range(1, len(fileArr)-1):
		    #     pName = fileArr[x].split("-")[0]
		    #     print(pName)
		    #     normVal = float(fileArr[x].split("-")[1])
		    #     sgrecord[pName+"_norm"] = float(normVal); #unique string with parameters
		    #     if pName == "cf":
		    #         sgrecord[pName+"_natural"] = 440*np.power(2,normVal)
		    #         sgrecord["midi_num"] = freq2Midi(440*np.power(2,normVal))
		    #     elif pName == "rate":
		    #         sgrecord[pName+"_natural"]=np.power(2,normVal)
		    #     elif pName == "irreg":
		    #     	sgrecord[pName+"_natural"] = .04*np.power(10,normVal)
		    #     else:
		    #     	print("unrecognized param")

		    sgrecord["segment_number"] = fileArr[len(fileArr)-1].split("-")[1]
		    sgrecord["sound_name"] = fileArr[0]	
		    sgrecord["samplerate"] = self.sr; 
		    sgrecord["sound_source_int"] = self.srcType; #0 natural, 1 generated
		    sgrecord["sound_source_str"] = self.srcType_string
		    sgrecord["sound_source"] = self.soundSource
		    self.SGjson[filename]=sgrecord

	''' Stores records one at a time'''
	def storeSingleRecord(self,filename):
	    sgrecord = {}
	    sgrecord["sound_name"] = filename
	    fileArr = os.path.splitext(filename)[0].split("--")
	    sgrecord["sound_name"] = fileArr[0]
	    sgrecord["samplerate"] = self.sr; 
	    sgrecord["sound_source_int"] = self.srcType; #0 natural, 1 generated
	    sgrecord["sound_source_str"] = self.srcType_string
	    sgrecord["sound_source"] = self.soundSource
	    self.SGjson[filename]=sgrecord

	def addParams(self,filename,pName, normVal, naturalVal):
		sgrecord = self.SGjson[filename]
		sgrecord[pName+"_norm"] = float(normVal)
		sgrecord[pName+"_natural"] = float(naturalVal)
		if pName == "cf":
			sgrecord["midi_num"] = freq2Midi(naturalVal)
		self.SGjson[filename]=sgrecord

	def printRecord(self,fileName):
		print(json.dumps(self.SGjson[fileName], indent=4, sort_keys=True))

	def ppRecords(self):
		print(json.dumps(self.SGjson, indent=4, sort_keys=True))

	def write2File(self,filename):
		with open(os.path.join(self.outPath,filename), 'w') as outfile:
			json.dump(self.SGjson, outfile, indent=4, sort_keys=True)
		print("written output to ", filename)

# Freq to MIdi for datasets with center frequency
def freq2Midi(freq):
	return round(12*math.log2(freq/440))+69;
