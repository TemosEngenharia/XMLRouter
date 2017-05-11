
#
# ATT 2017-05-09 ATT v0.1
#
# TOOLS FOR XML RENAME TO ORIGINAL FILE NAME
#
#

import xml_router_config as config 


#Logging Required Imports
import logging_config as lc
import logging



import datetime


from os import listdir
from os.path import isfile, join
from os import walk
from os import rename
import errno
import os

def writeOut(outputText, filename):
	with open(filename,"w+") as f:
		f.write(outputText)



def strip_one_space(s):
    if s.endswith(" "): s = s[:-1]
    if s.startswith(" "): s = s[1:]
    return s



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


#---------------------------------------------------
def main():
	#Load Logging Default Config
	lc.setup_logging()
	logger = logging.getLogger(__name__)

	logger.info("----- -> START_UP <- "+"-"*50)

	#Start Up Settings
	config.init("dev_mode")

	logger.info(config.settings)


	#file_prefix = 'COR'
	
	#config.inputXMLPath = "../OdooImporterData/corretiva/xml/QUEUE/REVIEW/" # + file_prefix + "/"
	config.inputXMLPath = "RENAMEBACK/"

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
			
			#logger.info(config.inputXMLFile)
			logger.info("["+str(counter)+"]> > > Processing XML Doc:" + config.inputXMLFile)

			#Get New Filename
			source = config.inputXMLPath + filename
			
			fileAttributes = filename.split("__")

			destination = config.inputXMLPath + fileAttributes[len(fileAttributes)-1]

			if len(destination)>0:
				logger.info("rename from source:" + source)
				logger.info("rename to destination:" + destination)

				status = True
			else:
				status = False
			
		except Exception as e:
			#raise e
			logger.error("Error:" + config.inputXMLFile + "\n" + str(e))
			logger.error('Error detail:', exc_info=True)

			status = False

		logger.info(" -> #EOF status:" + str(status))		

		#Rename To Original
		if status==True:
			rename(source, destination)


	logger.info("----- -> THE END <- "+"-"*50)



#---------------------------------------------------
if __name__ == "__main__":
	main()








