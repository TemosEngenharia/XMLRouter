
#
# ATT 2017-05-08 ATT v0.1
#
# TOOLS FOR XML FILE ROUTING
#
#

import xml_router_config as config 

#Logging Required Imports
import logging_config as lc
import logging

import datetime

import os
from os import listdir
from os.path import isfile, join
#from os import walk
from os import rename

def ensure_dir(dirname):
	logger = logging.getLogger(__name__)
	
	if not os.path.exists(dirname):

		logger.warn('Path %s not exists! Creating... ', dirname)

		try:
			#os.makedirs(dirname) old python
			os.makedirs(dirname, exist_ok=True)

		except OSError as exception:
			
			logger.error('Creating path %s failed... ', dirname)	        
			logger.error('Error detail:', exc_info=True)
			
			if exception.errno != errno.EEXIST:
				raise

def writeOut(outputText, filename):
	with open(filename,"w+") as f:
		f.write(outputText)



def strip_one_space(s):
    if s.endswith(" "): s = s[:-1]
    if s.startswith(" "): s = s[1:]
    return s



#---------------------------------------------------
def main():

	#Load Logging Default Config
	lc.setup_logging()
	logger = logging.getLogger(__name__)

	logger.info("----- -> START_UP <- "+"-"*50)

	#Start Up Settings
	config.init("dev_mode")

	#file_prefix = 'COR'

	#Force path creation
	ensure_dir(config.inputXMLPath)

	files = []
	try:
		files = [f for f in listdir(config.inputXMLPath) if isfile(join(config.inputXMLPath, f))]
		logger.info("Verifing contents of folder:" + config.inputXMLPath)
		logger.info("files in folder:"+str(len(files)))

	except Exception as e:
		#raise e
		logger.info("Error:" + config.inputXMLPath + "\n" + str(e))

		status = False	

	

	counter = 0

	#Process all
	for filename in files:

		counter = counter + 1

		try:

			config.inputXMLFileName = filename
			config.inputXMLFile = config.inputXMLPath + config.inputXMLFileName
			
			logger.info("["+str(counter)+"]> > > Processing XML Doc:" + config.inputXMLFile)

			xmldoc_Parsed_Root = config.etree.parse(config.inputXMLFile).getroot()

			#Get Form Name From XML File
			config.formName = xmldoc_Parsed_Root.xpath(config.formNameXPath)[0].text.upper()
			logger.info("Form Name:" + config.formName)

			#Only Allowed Prefixed Names will be processed
			if config.formName[:config.prefixLen] in config.allowedFormPrefixList:

				#Get Form Version
				config.formVersion = xmldoc_Parsed_Root.xpath(config.formVersionXPath)[0].text.upper()
				logger.info("Version:" + config.formVersion)


				#Get Form Date from Epoch and convert-it
				config.formDateFromEpoch = xmldoc_Parsed_Root.xpath(config.formDateFromEpochXPath)[0].text

				config.formDateTime = config.convertDateTimeFromEpochDateTime(config.formDateFromEpoch)

				logger.info("Data/Hora BR:" + '{:%Y%m%d-%H%M%S}'.format(config.formDateTime))


				formDateString = xmldoc_Parsed_Root.xpath("/Entry/EntryDate")[0].text

				logger.info(str(formDateString))


				if config.formName[:config.prefixLen] == "INV":
					
					config.formVehicleNumber = xmldoc_Parsed_Root.xpath(config.formVehicleNumberXPath)[0].text

					config.formVehicleNumber = config.formVehicleNumber.upper()

					config.formVehicleNumber = config.formVehicleNumber.replace('-', '')

					config.formVehicleNumber = config.formVehicleNumber.replace(' ', '')

					logger.info("Vehicle Number:" + config.formVehicleNumber)

					#pos = xmldoc_Parsed_Root.xpath("count(/Entry/Form/Fields/Field[.='Placa da Viatura']/preceding-sibling::*)+1.")
						
					#print("position:" + str(pos))				


				#Get New Filename
				source = config.inputXMLPath + filename
				destination = config.getFileDestination(filename)
				
				if len(destination)>0:
					logger.info("source:" + source)
					logger.info("destination:" + destination)
					status = True
				else:
					status = False
			else:	
				logger.warn("No valid file prefix allowed:" + file)
				status = False
			
		except Exception as e:
			#raise e
			logger.error("Error:" + config.inputXMLFile + "\n" + str(e))
			logger.error('Error detail:', exc_info=True)

			status = False

		logger.info(" -> #EOF status:" + str(status))	

		#move file to OK Subfolder
		if status==True:
			rename(source, destination)

		#move file to ERRORS Subfolder
		#if status==False:
			#rename(config.inputXMLFile, config.inputXMLPath + "ERRORS/" + config.inputXMLFileName)	

	logger.info("----- -> THE END <- "+"-"*50)



#---------------------------------------------------
if __name__ == "__main__":
	main()








