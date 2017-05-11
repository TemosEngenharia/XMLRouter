
#
# ATT 2017-05-08 v0.1 ATT - Config file
#
# TOOLS
#
# SETTINGS
#
import time
from datetime import datetime, timezone #Py3
import pytz
import os, errno

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")



def ensure_dir(dirname):
    """
    Ensure that a named directory exists; if it does not, attempt to create it.
    """
    try:
        os.makedirs(dirname)
    except OSError:
        pass


#Return Formatted Date from timestamp in miliseconds
def convertDateTimeFromEpochDateTime(datetime_from_epoch_ms):
  return datetime.fromtimestamp(int(datetime_from_epoch_ms)/1000, pytz.timezone('America/Sao_Paulo')) #timezone.utc)

#Get Path Destination based on 3 chars prefix
def getFileDestination(old_filename):
  prefix = formName[:prefixLen]
  prefix = prefix.upper()

  if prefix in ["COR"]:

    #Corretiva
    newFileName = prefix+formVersion+separator+'{:%Y%m%d-%H%M%S}'.format(formDateTime)+separator+old_filename

    destinationDir = '../OdooImporterData/corretiva/xml/QUEUE/'
    
    ensure_dir(destinationDir)

  elif prefix in ["INV"]:
    newFileName = prefix+formVersion+separator+formVehicleNumber+separator+'{:%Y%m%d-%H%M%S}'.format(formDateTime)+separator+old_filename

    destinationDir = '../OdooImporterData/inventario/xml/QUEUE/'
    
    ensure_dir(destinationDir)

    return  destinationDir + newFileName

  elif prefix in ["PRED"]:
    destinationDir = '../OdooImporterData/preditiva/xml/QUEUE/'
    
    ensure_dir(destinationDir)

  else:
    destinationDir=""
    newFileName=""

  print("dir"+destinationDir)
  print("newfilename"+newFileName)

  return  destinationDir + newFileName



def init(arg):
	
  global settings
  settings = []
  settings.append(arg)

  global inputXMLPath

  inputXMLPath = "INBOX/"

  global errorsXMLPath
  errorsXMLPath = inputXMLPath + "ERRORS/"

  #custom global var
  global formName, formNameXPath
  global formDateTime,formDateFromEpoch, formDateFromEpochXPath
  global formVersion, formVersionXPath
  global formVehicleNumber, formVehicleNumberXPath

  formNameXPath = "/Entry/Form/Name"
  formVersionXPath = "/Entry/Form/Version"
  formDateFromEpochXPath = "/Entry/EntryDateFromEpoch"
  formVehicleNumberXPath = "/Entry/Form/Fields/Field[Id='Placa da Viatura']/Value"

  global prefixLen
  prefixLen=3

  global separator
  separator = "__"

  global allowedFormPrefixList
  allowedFormPrefixList = ["COR","INV","PRE"]


