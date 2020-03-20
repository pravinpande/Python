#************************************************************************************
#EXPORT ACTION
#11.1.2.4.220
#************************************************************************************

def export(fdmAPI,fdmContext):
  
  #************************************************************************************
  #Build query to get max custom dims
  #************************************************************************************
  def getMaxCustomDims(appID):
    #return "SELECT COUNT(BALANCE_COLUMN_NAME) FROM AIF_TARGET_APPL_DIMENSIONS WHERE APPLICATION_ID = ? AND BALANCE_COLUMN_NAME IS NOT NULL AND BALANCE_COLUMN_NAME LIKE 'UD%' AND TARGET_DIMENSION_CLASS_NAME <> 'LOOKUP'"
    return "SELECT COUNT(BALANCE_COLUMN_NAME) FROM AIF_TARGET_APPL_DIMENSIONS WHERE APPLICATION_ID = " + appID + " AND BALANCE_COLUMN_NAME IS NOT NULL AND BALANCE_COLUMN_NAME LIKE 'UD%' AND TARGET_DIMENSION_CLASS_NAME <> 'LOOKUP'"
  
  def generateFXRatesLoadFile(loadID,strFile,hfmAPI,fdmAPI,fxEntity,beginAccount,endAccount,averageAccount):
    import codecs
    import os
    colName = ""
    DELIM = ";"
    
    objFile = codecs.open(strFile,"a", "UTF-16_LE")
        
    if fxEntity == "IsEmpty":
      objFile.write("!Entity = [None]" + os.linesep)
      objFile.write("!Value = [None]" + os.linesep)
    else:
      objFile.write("!Entity = " + fxEntity + os.linesep)
      
      #************************************************************************************
      #Get the location's DataValue
      #************************************************************************************
      rs = fdmAPI.getLocationDetails(BigDecimal(str(fdmContext["LOCKEY"])))
      while(rs.next()):
        strDataValue = rs.getString("PARTDATAVALUE")
      
      #If data value is not set default to <entity currency>
      if strDataValue == None:
        strDataValue = "<entity currency>"
      
      Position = strDataValue.find(DELIM)
      if Position > 0:
        strDataValue = strDataValue[:Position]
      
      objFile.write("!Value = " + strDataValue + os.linesep)
      #************************************************************************************

    objFile.write("!ICP = [ICP None]" + os.linesep)
    objFile.write("!VIEW = YTD" + os.linesep)
    
    try:
      rs = hfmAPI.getActiveTargetDims(False)
      while(rs.next()):
        colName = rs.getString("TDATASEG_COLUMN")
        if colName.startswith("UD"):
          if colName != "UD1" and colName != "UD2":
            objFile.write("!" + rs.getString("DIMENSION_NAME"))
            objFile.write(" = [None]")
            objFile.write(os.linesep)
    except:
      fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
      objFile.close
      return False
    
    objFile.write(os.linesep)
    objFile.write("!Data" + os.linesep)
    
    try:
      fxSQL = "SELECT (SELECT A.CATNAME FROM TPOVCATEGORY A INNER JOIN AIF_BAL_RULE_LOADS B ON A.CATKEY = B.CATKEY WHERE B.LOADID = " + loadID + ") as CATNAME, EPM_YEAR, EPM_PERIOD, FROM_CURRENCY, TO_CURRENCY, RATE_TYPE, CONVERSION_RATE FROM AIF_HS_EXCHANGE_RATES WHERE LOADID = " + loadID + " ORDER BY RATE_TYPE"
      rs = fdmAPI.executeQuery(fxSQL, None)      
      while(rs.next()):
        
        objFile.write(rs.getString("CATNAME") + DELIM)
        objFile.write(rs.getString("EPM_YEAR") + DELIM)
        objFile.write(rs.getString("EPM_PERIOD") + DELIM)
        
        if rs.getString("RATE_TYPE") == "BEGIN":
          objFile.write(beginAccount + DELIM)
        elif rs.getString("RATE_TYPE") == "END":
          objFile.write(endAccount + DELIM)
        elif rs.getString("RATE_TYPE") == "AVERAGE":
          objFile.write(averageAccount + DELIM)
          
        objFile.write(rs.getString("FROM_CURRENCY") + DELIM)
        objFile.write(rs.getString("TO_CURRENCY") + DELIM)
        objFile.write(str(rs.getBigDecimal("CONVERSION_RATE",38)))
        objFile.write(os.linesep)
        
    except:
      fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
      fdmAPI.logError(str(fxSQL).encode("utf-8"))
      objFile.close
      return False
    
    objFile.close
    return True
  
  def exportICP(fileName,rs,fdmCustoms):
    import codecs
    import os
    
    #CONSTANTS
    DELIM = ";"
    if rs == None:
      return False
    
    objFile = codecs.open(strFile,"a", "UTF-16_LE")
      
    objFile.write("!InterCompany Detail" + os.linesep)
    objFile.write("!Column_Order = ")
    objFile.write("Entity" + DELIM)
    objFile.write("Partner" + DELIM)
    objFile.write("Account" + DELIM)
    objFile.write("C1" + DELIM)
    objFile.write("C2" + DELIM)
    
    x = 1
    while x <= fdmCustoms:
      objFile.write("C" + str((x + 2)) + DELIM)
      x += 1
    
    objFile.write("TransID" + DELIM)
    objFile.write("SubID" + DELIM)
    objFile.write("RefID" + DELIM)
    objFile.write("Date" + DELIM)
    objFile.write("EntCurrAmt" + DELIM)
    objFile.write("TransCurr" + DELIM)
    objFile.write("Rate" + DELIM)
    objFile.write("Comment1" + DELIM)
    objFile.write("TransAmt" + os.linesep)
    
    currentScenario = ""
    scenario = ""
    currentYear = ""
    year = ""
    currentPeriod = ""
    period = ""
    
    while(rs.next()):
      currentScenario = rs.getString("SCENARIO")
      if currentScenario != scenario:
        objFile.write("!Scenario=" + currentScenario + os.linesep)
      
      currentYear = rs.getString("YEAR")
      if currentYear != year:
        objFile.write("!Year=" + currentYear + os.linesep)
      
      currentPeriod = rs.getString("PERIOD")
      if currentPeriod != period:
        objFile.write("!Period=" + currentPeriod + os.linesep)
      
      objFile.write(rs.getString("ENTITY") + DELIM)
      objFile.write(rs.getString("ICP") + DELIM)
      objFile.write(rs.getString("ACCOUNT") + DELIM)
      objFile.write(rs.getString("UD1") + DELIM)
      objFile.write(rs.getString("UD2") + DELIM)
      
      x = 1
      while x <= fdmCustoms:
        objFile.write(rs.getString("UD" + str((x + 2))) + DELIM)
        x += 1
      
      #TransID
      if rs.getString("ATTR1") != None:
        objFile.write(rs.getString("ATTR1") + DELIM)
      else:
        objFile.write(DELIM)
      
      #SubID
      if rs.getString("ATTR2") != None:
        objFile.write(rs.getString("ATTR2") + DELIM)
      else:
        objFile.write(DELIM)
      
      #RefID
      if rs.getString("ATTR3") != None:
        objFile.write(rs.getString("ATTR3") + DELIM)
      else:
        objFile.write(DELIM)
      
      #Date
      if rs.getString("ATTR4") != None:
        objFile.write(rs.getString("ATTR4") + DELIM)
      else:
        #date is required
        objFile.write('12/31/2014;')
      
      #EntCurrAmt
      if rs.getString("ATTR5") != None:
        objFile.write(rs.getString("ATTR5") + DELIM)
      else:
        objFile.write(DELIM)
      
      #TransCurr
      if rs.getString("ATTR6") != None:
        objFile.write(rs.getString("ATTR6") + DELIM)
      else:
        objFile.write(DELIM)
      
      #Rate
      if rs.getString("ATTR7") != None:
        objFile.write(rs.getString("ATTR7") + DELIM)
      else:
        objFile.write(DELIM)
      
      #Comment1 
      if rs.getString("ATTR11") != None:
        objFile.write(rs.getString("ATTR11") + DELIM)
      else:
        objFile.write(DELIM)
      
      #TransAmt
      objFile.write(rs.getString("AMOUNT") + os.linesep)
      
      scenario = currentScenario
      year = currentYear
      period = currentPeriod
  
    objFile.close()
    return True
  
  
  
  
  
  #************************************************************************************
  #End of Utility Methods
  #************************************************************************************
  
  #************************************************************************************
  #EXPORT ACTION
  #************************************************************************************
  
  #************************************************************************************
  #Import Required Libraries
  #************************************************************************************
  import sys
  import os
  import codecs
  import java.math.BigDecimal as BigDecimal
  import java.util.ArrayList as ArrayList
  import java.util.TreeMap as TreeMap
  import com.hyperion.aif.hfm.HfmAdapter as HfmAdapter
  import com.hyperion.aif.hfm.ProtectionData as ProtectionData
  #************************************************************************************
  
  try: #instantiate adapter
    hfmAdapter = HfmAdapter()
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    fdmAPI.logError("Could not instantiate the HfmAdapter.")
    return False
  
  userName = unicode(fdmContext["USERNAME"])
  
  locale = unicode(fdmContext["USERLOCALE"])
  
  if locale == "None":
    fdmAPI.logDebug("User Locale is not set. Defaulting to: en_US")
    locale = "en_US"
  else:
    fdmAPI.logDebug("User Locale is: " + locale)
  
  #************************************************************************************ 
  #CONSTANTS
  #************************************************************************************
  PROCESS_EXPORT = "PROCESS_BAL_EXP_HFM"
  PROCESS_RATES = "PROCESS_EXCHANGE_RATE_LOAD_HFM"
  PROCESS_RUNNING = "RUNNING"
  PROCESS_SUCCESS = "SUCCESS"
  PROCESS_FAILED = "FAILED"
  DELIM = ";"
  #************************************************************************************
  
  #************************************************************************************ 
  #generate path for .dat file
  #************************************************************************************
  strFile = "%s\%s_%s.dat" %(fdmContext["OUTBOXDIR"], fdmContext["APPNAME"], str(fdmContext["LOADID"]))
  strFile = strFile.replace('\\','/')
  strFile = os.path.normpath(strFile)
  #************************************************************************************
  
  #************************************************************************************
  #Initialize the adapter
  #************************************************************************************
  try:
    hfmAdapter.init(fdmContext["LOADID"])

    #Create an entry for the Process Details
    fdmAPI.insertIntoProcessDetails(PROCESS_EXPORT,fdmContext["APPNAME"], PROCESS_RUNNING)
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    hfmAdapter.close()
    fdmAPI.insertIntoProcessDetails(PROCESS_EXPORT,fdmContext["APPNAME"], PROCESS_FAILED)
    return False
  
  #************************************************************************************
  #Get HFM Cluster
  #************************************************************************************
  try:
    fmCluster = hfmAdapter.getHfmCluster(userName)
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    fmCluster = "HFMCluster"
  #************************************************************************************


  #************************************************************************************
  #Get the Target System Options
  #************************************************************************************
  try:
    #get adapter options
    rs = hfmAdapter.getAdapterOptionsForLoadID()
    
    TargetOptions = TreeMap()
    while(rs.next()):
      TargetOptions.put(rs.getString("PARAMETER_NAME").upper(), rs.getString("PROPERTY_VALUE"))
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    hfmAdapter.close()
    return False
  #************************************************************************************
  
  #************************************************************************************
  #Check for Global Login ID
  #************************************************************************************
  globalID = hfmAdapter.getGlobalUserID()
  fdmAPI.logDebug("Global User ID: " + str(globalID).encode("utf-8"))
  if globalID != "":
    userName = globalID 
  #************************************************************************************
  
  #************************************************************************************
  #Connect to HFM
  #************************************************************************************
  isConnectedForLineItems = False
  isConnectedForDataProtection = False
  #try:
  #  isConnected = hfmAdapter.connect(userName, locale, fmCluster, unicode(fdmContext["TARGETAPPNAME"]))
  #  if isConnected == False:
  #    fdmAPI.logError("Failed to connect to:%s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
  #    fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
  #    hfmAdapter.close()
  #    return False
  #  else:
  #    fdmAPI.logDebug("Connected to: %s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
  #except:
  #  fdmAPI.logError("Failed to connected to: %s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
  #  hfmAdapter.close()
  #  return False
   
  #************************************************************************************
  
  #************************************************************************************
  #Get Max Custom Dimensions
  #************************************************************************************
  try:
    #Get Max custom dims being loaded to target
    strSQL = getMaxCustomDims(str(fdmContext["APPID"]))
    rs = fdmAPI.executeQuery(strSQL, None)
    while(rs.next()):
      fdmCustoms = int(rs.getString(1)) - 2
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    fdmAPI.logError(str(strSQL).encode("utf-8"))
    hfmAdapter.close()
    return False
  #************************************************************************************
  
  #************************************************************************************
  #Get the location's DataValue
  #************************************************************************************
  rs = fdmAPI.getLocationDetails(BigDecimal(str(fdmContext["LOCKEY"])))
  while(rs.next()):
    strDataValue = rs.getString("PARTDATAVALUE")
  
  #If data value is not set default to <entity currency>
  if strDataValue == None:
    strDataValue = "<entity currency>"
  #************************************************************************************
  
  #************************************************************************************
  #Check Journal Loading Options
  #************************************************************************************
  Position = strDataValue.find(DELIM)
  if bool(int(TargetOptions.get("ENABLE_JOURNAL_LOAD"))) == True:
    if Position > 0:
      blnLoadAsJournals = True
    else:
      blnLoadAsJournals = False
  else:
    blnLoadAsJournals = False
  
  if Position > 0:
    strDataValue = strDataValue[:Position]
  
  if strDataValue.lower() in ("<entity curr adjs>", "<parent curr adjs>", "[contribution adjs]", "[parent adjs]"):
    if blnLoadAsJournals == False:
      #DataValue Requires Journal Loading, Set to false and load as entity currency
      blnDataAsJournal = False
      strDataValue = "<Entity Currency>"
    else:
      blnDataAsJournal = True
  else:
    blnDataAsJournal = False
  #************************************************************************************
  
  #Default to True
  bolResult = True
  datFileCreated = False
  loadFXRates = False
  
  #************************************************************************************
  #Check for FX Rate Load Option
  #************************************************************************************
  try:
    strSQL = "Select LOAD_EXCHANGE_RATE_FLAG From AIF_BAL_RULE_LOADS WHERE LOADID = %s AND LOAD_EXCHANGE_RATE_FLAG IS NOT NULL" % str(fdmContext["LOADID"]) 
    rs = fdmAPI.executeQuery(strSQL, None)
    while(rs.next()):
      loadFXRates = True
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    fdmAPI.logError(str(strSQL).encode("utf-8"))
    loadFXRates = False
  
  if loadFXRates == True:
    strFXRatesFile = "%s\%s_%s_FXRates.dat" %(fdmContext["OUTBOXDIR"], fdmContext["APPNAME"], str(fdmContext["LOADID"]))
    strFXRatesFile = strFXRatesFile.replace('\\','/')
    strFXRatesFile = os.path.normpath(strFXRatesFile)
    
    #Get the Global Adapter Options - Only these contain the currency rate account options
    beginAccount = "[None]"
    endAccount = "[None]"
    averageAccount = "[None]"
    fxEntity = "IsEmpty"
    
    try:
      rs = hfmAdapter.getAdapterOptions()
      while(rs.next()):        
        if rs.getString("LOOKUP_CODE") == "CURR_RATE_ACCT_BEGIN_RATE":
          if rs.getString("PROPERTY_VALUE") != None:
            beginAccount = rs.getString("PROPERTY_VALUE")
        elif rs.getString("LOOKUP_CODE") == "CURR_RATE_ACCT_END_RATE":
          if rs.getString("PROPERTY_VALUE") != None:
            endAccount = rs.getString("PROPERTY_VALUE")
        elif rs.getString("LOOKUP_CODE") == "CURR_RATE_ACCT_AVG_RATE":
          if rs.getString("PROPERTY_VALUE") != None:
            averageAccount = rs.getString("PROPERTY_VALUE")
        elif rs.getString("LOOKUP_CODE") == "CURR_RATE_ENTITY":
          if rs.getString("PROPERTY_VALUE") != None:
            fxEntity = rs.getString("PROPERTY_VALUE")

    except:
      fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
      hfmAdapter.close()
      return False
    
    if (generateFXRatesLoadFile(str(fdmContext["LOADID"]),strFXRatesFile,hfmAdapter,fdmAPI,fxEntity,beginAccount,endAccount,averageAccount)) == False:
      fdmAPI.insertIntoProcessDetails(PROCESS_RATES,fdmContext["APPNAME"], PROCESS_FAILED)
      fdmAPI.logDebug("Export Exchange Rates failed.")
    else:
      fdmAPI.insertIntoProcessDetails(PROCESS_RATES,fdmContext["APPNAME"], PROCESS_RUNNING)
  
  
  #************************************************************************************
  #Are we loading data as journal? If so, exit the Export script and enter the Load script
  #************************************************************************************  
  if blnDataAsJournal == True:
  
    #Check the journal numbering switch
    blnJournalIDPerEntity = bool(int(TargetOptions.get("ENABLE_JOURNAL_JVID_ENTITY")))
  
    #Set the journal ID based on the numbering type (Single ID or One Per Entity)
    if blnJournalIDPerEntity == True:
      try:
        #Execute Journal Entry Number Per Entity
        bolResult = hfmAdapter.setJournalNumberPerEntity()
      except:
        fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
        fdmAPI.logError(str(strSQL).encode("utf-8"))
        hfmAdapter.close()
        bolResult = False
    else:
      #Execute the single journal entry number update
      try:
        #rowsAffected = fdmAPI.executeDML(strSQL,None,True)
        rowsAffected = hfmAdapter.setJournalNumberAll()
        if rowsAffected > 0:
          bolResult = True
      except:
        fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
        fdmAPI.logError(str(strSQL).encode("utf-8"))
        hfmAdapter.close()
        bolResult = False
    
    #Check the result of journal number setting
    if bolResult == True:
      #Create an empty file stating "Data Loaded as Journal"
      objFile = codecs.open(strFile,"w", "UTF-16_LE")
        
      strFile = "%s\%s_%s.jlf" %(fdmContext["OUTBOXDIR"], fdmContext["APPNAME"], str(fdmContext["LOADID"]))
      strFile = strFile.replace('\\','/')      
      objFile.write("All data loaded as a Journal.  See the Journal Data file (" + strFile + ") contents.")
      objFile.close()
      
      fdmAPI.updateProcessDetails(PROCESS_SUCCESS, PROCESS_EXPORT)
      fdmAPI.logDebug("Data as Journal detected. Journal File will be created in the HFM_LOAD.py Action Script.")
    else:
      fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
      fdmAPI.logDebug("Data as Journal detected, but there was an error updating the Journal number.")
      hfmAdapter.close()
      return False

    #Data As Journal - No errors: HFM_LOAD.py handles the rest.
    hfmAdapter.close()
    return True
  #************************************************************************************  
  if hfmAdapter.doesLoadIDLoadICP() == True:
    if hfmAdapter.importFormatLoadsIcp() == True:
      strFile = "%s\%s_%s.trn" %(fdmContext["OUTBOXDIR"], fdmContext["APPNAME"], str(fdmContext["LOADID"]))
      strFile = strFile.replace('\\','/')
      strFile = os.path.normpath(strFile)
      
      rsICP = hfmAdapter.getTrialBalanceIcp()
      if hfmAdapter.generateUnicodeFile(strFile) != True:
        fdmAPI.logError("Failed to generate ICP Load file.")
        fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
        hfmAdapter.close()
        return False
      else:
        if (exportICP(strFile,rsICP,fdmCustoms) == True):
          fdmAPI.updateProcessDetails(PROCESS_SUCCESS, PROCESS_EXPORT)
          fdmAPI.logDebug("IC Detail Export was successful. See %s" % str(strFile).encode("utf-8"))
          return True
        else:
          fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
          fdmAPI.logDebug("IC Detail Export failed.")
          hfmAdapter.close()
          return False
  
  #*******************************************************************
  #Line Item Detail Processing
  #*******************************************************************
  loadLineItems = bool(int(TargetOptions.get("LOAD_LINE_ITEM_DETAIL")))
  lidLoadType = TargetOptions.get("LID_LOAD_TYPE")
  
  try:
    rsActiveDims = hfmAdapter.getActiveTargetDims(True)
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    hfmAdapter.close()
    return False
  
  if blnLoadAsJournals == True:

    fdmAPI.logDebug( "***Export data as data and journals as journals***" )
    #exclude FDM Journals from DAT file
    strSelect = "SELECT "
    strFrom = " FROM AIF_HS_BALANCES"
    strGroupBy = " GROUP BY SCENARIO, PERIOD, DATAVIEW, ENTITY, "
    strWhere = " WHERE LOADID = " + str(fdmContext["LOADID"])
    strWhere += " AND (" + fdmAPI.getDBProperties()["LENGTH_FUNCTION"] + "(JournalID) = 0 OR JournalID Is Null)"
    
    while(rsActiveDims.next()):
      strSelect += rsActiveDims.getString("TDATASEG_COLUMN") + ", "
      
      if rsActiveDims.getString("TDATASEG_COLUMN") <> "ENTITY":
        strGroupBy += rsActiveDims.getString("TDATASEG_COLUMN") + ", "
    
    strSelect = strSelect + "YEAR as YEAR, PERIOD as PERIOD, SCENARIO AS SCENARIO, DATAVIEW AS DATAVIEW, DATAVALUE AS VALUE, SUM(AMOUNT) AS AMOUNT, JOURNALID as JOURNALID"
    strGroupBy = strGroupBy + "YEAR,PERIOD,SCENARIO,DATAVIEW,DATAVALUE,JOURNALID"
    
  else:
    fdmAPI.logDebug( "***Export data and Journals as data***" )
    #include both FDM Journals and standard data values
    strSelect = "SELECT "
    strFrom = " FROM AIF_HS_BALANCES"
    strGroupBy = " GROUP BY SCENARIO, PERIOD, DATAVIEW, "
    strWhere = " WHERE LOADID = " + str(fdmContext["LOADID"])
    
    while(rsActiveDims.next()):
      strSelect += rsActiveDims.getString("TDATASEG_COLUMN") + ", "
      strGroupBy += rsActiveDims.getString("TDATASEG_COLUMN") + ", "
    
    strSelect = strSelect + "YEAR as YEAR, PERIOD as PERIOD, SCENARIO AS SCENARIO, DATAVIEW AS DATAVIEW, DATAVALUE AS VALUE, SUM(AMOUNT) AS AMOUNT, JOURNALID as JOURNALID"
    strGroupBy = strGroupBy + "YEAR,PERIOD,SCENARIO,DATAVIEW,DATAVALUE,JOURNALID"
  
  rsExport = fdmAPI.executeQuery(strSelect + strFrom + strWhere + strGroupBy + " ORDER BY YEAR, PERIOD, SCENARIO, DATAVIEW, JOURNALID, ACCOUNT", None)

  while(rsExport.next()):
    if datFileCreated != True:
      if hfmAdapter.generateUnicodeFile(strFile) != True:
          fdmAPI.logError("Failed to generate data load file.")
          fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
          hfmAdapter.close()
          return False
      else:
        objFile = codecs.open(strFile,"a", "UTF-16_LE")
        
      objFile.write("!Data" + os.linesep)
      datFileCreated = True
      
    lidLinesWritten = False
    
    #Category
    strLine = rsExport.getString("SCENARIO") + DELIM
    
    #Year
    strLine += rsExport.getString("YEAR") + DELIM
  
    #Period
    strLine += rsExport.getString("PERIOD") + DELIM
  
    #View
    strLine += rsExport.getString("DATAVIEW") + DELIM
  
    #Entity
    strLine += rsExport.getString("ENTITY") + DELIM
  
    #DATAVALUE
    strLine += strDataValue + DELIM
    
    #ACCOUNT
    strLine += rsExport.getString("ACCOUNT") + DELIM
    
    #ICP
    strLine += rsExport.getString("ICP") + DELIM
    
    #C1
    strLine += rsExport.getString("UD1") + DELIM
    
    #C2
    strLine += rsExport.getString("UD2") + DELIM
    
    x = 1
    while x <= fdmCustoms:
      strLine += rsExport.getString("UD" + str((x + 2))) + DELIM
      x += 1
    
    #Line Item Detail
    if loadLineItems == True:
      #************************************************************************************
      #Connect to HFM
      #************************************************************************************
      if isConnectedForLineItems == False:
        try:
          isConnectedForLineItems = hfmAdapter.connect(userName, locale, fmCluster, unicode(fdmContext["TARGETAPPNAME"]))
          if isConnectedForLineItems == False:
            fdmAPI.logError("Failed to connect to:%s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
            fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
            hfmAdapter.close()
            return False
          else:
            fdmAPI.logDebug("Connected to: %s for line items" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
        except:
          fdmAPI.logError("Failed to connected to: %s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
          hfmAdapter.close()
          return False
      
      if hfmAdapter.accountUsesLineItems(unicode(rsExport.getString("ACCOUNT")))== True:       
        if lidLoadType == "1":
          #summary line items
          objFile.write("!LINE_ITEM_DETAIL" + os.linesep)
          
          #Amount, finish the line with normal length
          strLine += '"' + rsExport.getString("ACCOUNT") + '"' + DELIM + hfmAdapter.setAmountToHFMUserPref(rsExport.getString("AMOUNT"))
          
          #Write the line
          objFile.write(strLine + os.linesep)
          objFile.write("!DATA" + os.linesep)
        elif lidLoadType == "2":
          #DETAIL LINE ITEMS
          objFile.write("!LINE_ITEM_DETAIL" + os.linesep)

          aCustoms = ArrayList()
          
          x = 1
          while x <= (fdmCustoms + 2):
            aCustoms.add(rsExport.getString("UD" + str((x))))
            x += 1
          
          try:
            rsDrill = hfmAdapter.getLineItemDetail(unicode(rsExport.getString("SCENARIO")),
                                            unicode(rsExport.getString("PERIOD")),
                                            unicode(rsExport.getString("YEAR")),
                                            unicode(rsExport.getString("DATAVIEW")),
                                            unicode(rsExport.getString("ENTITY")),
                                            unicode(rsExport.getString("ACCOUNT")),
                                            unicode(rsExport.getString("ICP")),
                                            aCustoms)
            
            while(rsDrill.next()):                
              #Write the DETAIL line to the file
              try:
                amt = hfmAdapter.setAmountToHFMUserPref(rsDrill.getString("AMOUNTX"))
              except:
                amt = rsDrill.getString("AMOUNTX")
                
              lidLinesWritten = True
              objFile.write(strLine +
                            '"' +
                            unicode(rsDrill.getString("ACCOUNT")) + 
                            '-' + unicode(rsDrill.getString("ENTITY")) + 
                            '-' + unicode(rsDrill.getString("DESC1")) + 
                            '"' + 
                            DELIM + 
                            amt + 
                            os.linesep
                            )
          except:
            fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
            hfmAdapter.close()
            return False
          
          if lidLinesWritten == False:
            try:
              amt = hfmAdapter.setAmountToHFMUserPref(rsExport.getString("AMOUNT"))
            except:
              amt = rsExport.getString("AMOUNT")
              
            #finish line with normal length
            strLine += ('"' +
                        rsExport.getString("ACCOUNT") +
                        '"' +
                        DELIM +
                        amt
                        )
            objFile.write(strLine + os.linesep)
          
          objFile.write("!DATA" + os.linesep)
      else:
        try:
          strLine += hfmAdapter.setAmountToHFMUserPref(rsExport.getString("AMOUNT"))
        except:
          fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
          strLine += rsExport.getString("AMOUNT")
        
        objFile.write(strLine + os.linesep)
    else:
      try:
        #Check for Zero Suppression
        if bool(int(TargetOptions.get("HFM_ENABLE_MULTI_LOAD_LOADING"))):
          strLine += hfmAdapter.setAmountToHFMUserPref(rsExport.getString("AMOUNT"))
        else:
          if float(rsExport.getString("AMOUNT")) != 0:
            strLine += hfmAdapter.setAmountToHFMUserPref(rsExport.getString("AMOUNT"))
          else:
            strLine += ""
      except:
          fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
          strLine += rsExport.getString("AMOUNT")
      
      objFile.write(strLine + os.linesep)
  
  rsExport.close()
  
  #----------------------------------------------------------------------------
  #Data Protection - Extract Protection Data & Append to DAT file
  #----------------------------------------------------------------------------  
  if bool(int(TargetOptions.get("ENABLE_DATA_PROTECTION"))) == True:
    fdmAPI.logDebug("Data Protection is on.")
    
    #************************************************************************************
    #Connect to HFM
    #************************************************************************************
    if isConnectedForDataProtection == False:
      try:
        isConnectedForDataProtection = hfmAdapter.connect(userName, locale, fmCluster, unicode(fdmContext["TARGETAPPNAME"]))
        if isConnectedForDataProtection == False:
          fdmAPI.logError("Failed to connect to:%s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
          fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
          hfmAdapter.close()
          return False
        else:
          fdmAPI.logDebug("Connected to: %s for data protection" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
      except:
        fdmAPI.logError("Failed to connected to: %s" % str(fdmContext["TARGETAPPNAME"]).encode("utf-8"))
        hfmAdapter.close()
        return False
    
    try:
      extractedProtectionData = hfmAdapter.extractDataProtection(fdmContext["OUTBOXDIR"], 
                                                                 DELIM, 
                                                                 TargetOptions.get("PROTECTION_OPERATOR"), 
                                                                 TargetOptions.get("PROTECTION_VALUE"), 
                                                                 False, 
                                                                 False)
    except:
      fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
      hfmAdapter.close()
      return False
      

    fdmAPI.logDebug("ppodhiya - Before check")
    if extractedProtectionData.size() > 0:
      fdmAPI.logDebug("ppodhiya - After check. Size > 0")
      objFile.write(os.linesep)
      objFile.write("'The following data is added to this file as a result of Data Protection" + os.linesep)
      blnCellText = False
      for pData in extractedProtectionData:
        if pData.find("!DESCRIPTIONS") != -1:
          fdmAPI.logDebug("ppodhiya - *************** Found Cell Text Section ***************")
          fdmAPI.logDebug("ppodhiya - Setting blnCellText to True to skip cell text data")
          blnCellText = True
        if blnCellText == False:
          objFile.write (pData + os.linesep)
      #END FOR
      objFile.write(os.linesep)

  #END IF - DATA PROTECTION
  if datFileCreated == True:
    objFile.close()
  else:
    if hfmAdapter.generateUnicodeFile(strFile) != True:
        fdmAPI.logError("Failed to generate data load file.")
        fdmAPI.updateProcessDetails(PROCESS_FAILED, PROCESS_EXPORT)
        hfmAdapter.close()
        return False
    else:
      objFile = codecs.open(strFile,"a", "UTF-16_LE")
      
    objFile.write("!DATA" + os.linesep)
    objFile.close()
    
  try:
    hfmAdapter.close()
  except:
    fdmAPI.logError(str(sys.exc_info()[1]).encode("utf-8"))
    hfmAdapter.close()
    return False
  
  #Update Export Status
  fdmAPI.updateProcessDetails(PROCESS_SUCCESS, PROCESS_EXPORT)


#************************************************************************************
#MAIN METHOD STARTS HERE
#************************************************************************************

#Log that the HFM Export process has started.
#************************************************************************************
fdmAPI.logDebug("************************************************************************************")
fdmAPI.logDebug("*      HFM_EXPORT.py Started for LoadID: %s" % str(fdmContext["LOADID"]))
fdmAPI.logDebug("************************************************************************************")
#************************************************************************************
result = export(fdmAPI,fdmContext)
if result == False:
  raise Exception("An error occurred during the Export.")
else:
  fdmAPI.logDebug("HFM Export Complete.")

fdmAPI.logDebug("************************************************************************************")
