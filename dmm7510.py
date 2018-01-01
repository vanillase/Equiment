import os,math,time,sys
import visa,csv,datetime

def dmm7510_dmm_loger_current(numofsamples='10000000',result_folder="C:\Temp\data.csv",samplerate='1000000',port='USB0::0x05E6::0x7510::04353687::INSTR'):
    try:
        result_csv = result_folder      
        rm = visa.ResourceManager()
        print rm.list_resources(port)
        print rm.list_resources_info(port)
        keithley = rm.open_resource(port)
        #Reset the instrument
        keithley.write('*RST')
        #Set the measurement function to Digitize Voltage to capture the power-up behavior
        keithley.write(':SENSe:DIGitize:FUNCtion "CURR"')
        #Current range must be fixed when using Digitizing Voltage
        keithley.write(':DIG:CURR:RANG 1')
        #Set the display resolution to the minimum - really only care about what's in the buffer
        keithley.write(':DISP:DIGitize:CURRent:DIG 3')
        #Set the sample rate to 1MHz to capture any glitch
        capture_rate=':SENSe:DIGitize:CURRent:SRATe '+samplerate
        keithley.write(capture_rate)
        #Set aperture to auto to get the highest accuracy measurement for the sampling rate configured
        keithley.write(':SENSe:DIGitize:CURRent:APERture AUTO')
        #Changing count is optional.  The reading buffer capacity is the determining factor
        caputre_count=':SENSe:DIG:COUN '+numofsamples
        keithley.write(caputre_count)
        #keithley.write(':FORM ASCii')
        #set digital io lines to be active,Set Digital I/O line 1 and 2 to be a digital line
        keithley.write(':DIG:LINE1:MODE TRIG, IN')
        #Set default buffer to minimum to allow for space in user define buffer memory
        keithley.write(':TRACe:POINts 10, "defbuffer1"')
        keithley.write(':TRACe:POINts 10, "defbuffer2"')
        #Set buffer3 as compact mode    
        makebuffer=':TRACe:MAKE "buffer3",'+numofsamples+', COMPact'
        keithley.write(makebuffer)
        #Set buffer fill up style
        keithley.write(':TRACe:FILL:MODE ONCE, "buffer3"')
        #Clear buffer
        keithley.write(':TRACe:CLEar "buffer3"')
        #set up trigger model
        keithley.write(':TRIG:LOAD "Empty"')
        keithley.write(':TRIGger:BLOCk:BUFFer:CLEar 1, "buffer3"')
        keithley.write(':TRIGger:BLOCk:WAIT 2, DIGio1')
        keithley.write(':TRIGger:BLOCk:DIGitize 3, "buffer3", '+numofsamples)
        #Start the trigger model
        keithley.write('INIT')
        #Postpone execution of subsequent commands until all previous commands are finished.
        keithley.write('*WAI')
        keithley.write(':SYSTem:BEEPer 500, 1')
        time.sleep(80)
        header= ["Reading","Time"]
        Result_file = open(result_csv,'wb') 
        spamwriter = csv.writer(Result_file,dialect='excel',quoting=csv.QUOTE_MINIMAL)    
        spamwriter.writerow(header)
        index=0
        enddata=keithley.query(':TRACe:ACTual:END? "buffer3"')
        print "Total data counts: %s"%enddata
        print "Saving data to %s"%result_csv
        #step = int(enddata)/1000000
        initial=1
        for count in range(1000000,int(enddata)+1,1000000):
            print "Print data from %d to %d"%(initial,count)
            voltage = keithley.query_ascii_values(':TRACe:DATA? '+str(initial)+', '+str(count)+',"buffer3", READ, REL')
            initial=count+1
            number =0
            data=[]
            for item in voltage:                            
                if (number %2) == 0 and len(data)>0:           
                    #print "%d\t%s\t%s\t"%(index,data[0],data[1]) 
                    spamwriter.writerow(data)        
                    index = index+1
                    data=[]
                    data.append(item)
                else:
                    data.append(item)
                number = number+1
        
    except KeyboardInterrupt:
        print "Interrupt happened. Close program gracefully."
        keithley.close()
        Result_file.close()
    finally:
        print "Data processing compeleted!"
        keithley.close()
        Result_file.close()        
def dmm7510_dmm_loger_voltage(numofsamples='10000000',result_folder="C:\Temp\data.csv",samplerate='1000000',port='USB0::0x05E6::0x7510::04353687::INSTR'):   
    try:
        result_csv = result_folder     
        rm = visa.ResourceManager()
        print rm.list_resources()
        keithley = rm.open_resource(port)
        #Reset the instrument
        keithley.write('*RST')
        #Set the measurement function to Digitize Voltage to capture the power-up behavior
        keithley.write(':SENSe:DIGitize:FUNCtion "VOLT"')
        #Current range must be fixed when using Digitizing Voltage
        keithley.write(':DIG:VOLT:RANG 10')
        #Set the display resolution to the minimum - really only care about what's in the buffer
        keithley.write(':DISP:DIGitize:VOLT:DIG 3')
        keithley.write(':DIG:VOLT:INP AUTO')
        #Set the sample rate to 1MHz to capture any glitch
        capture_rate=':SENSe:DIGitize:VOLT:SRATe '+samplerate
        keithley.write(capture_rate)
        #Set aperture to auto to get the highest accuracy measurement for the sampling rate configured
        keithley.write(':SENSe:DIGitize:VOLT:APERture AUTO')
        #Changing count is optional.  The reading buffer capacity is the determining factor
        caputre_count=':SENSe:DIG:COUN '+numofsamples
        keithley.write(caputre_count)
        #keithley.write(':FORM ASCii')
        #set digital io lines to be active,Set Digital I/O line 1 and 2 to be a digital line
        keithley.write(':DIG:LINE1:MODE TRIG, IN')
        #3keithley.write(':TRIGger:DIGital1:IN:EDGE EITHer')    
        #Set default buffer to minimum to allow for space in user define buffer memory
        keithley.write(':TRACe:POINts 10, "defbuffer1"')
        keithley.write(':TRACe:POINts 10, "defbuffer2"')
        #Set buffer3 as compact mode    
        makebuffer=':TRACe:MAKE "buffer3",'+numofsamples+', COMPact'
        keithley.write(makebuffer)
        #Set buffer fill up style
        keithley.write(':TRACe:FILL:MODE ONCE, "buffer3"')
        #Clear buffer
        keithley.write(':TRACe:CLEar "buffer3"')
        #set up trigger model
        keithley.write(':TRIG:LOAD "Empty"')
        keithley.write(':TRIGger:BLOCk:BUFFer:CLEar 1, "buffer3"')
        keithley.write(':TRIGger:BLOCk:WAIT 2, DIGio1')
        keithley.write(':TRIGger:BLOCk:DIGitize 3, "buffer3", '+numofsamples)
        #Start the trigger model
        keithley.write('INIT')
        #Postpone execution of subsequent commands until all previous commands are finished.
        keithley.write('*WAI')
        keithley.write(':SYSTem:BEEPer 500, 1')
        time.sleep(80)
        header= ["Reading","Time"]
        Result_file = open(result_csv,'wb') 
        spamwriter = csv.writer(Result_file,dialect='excel',quoting=csv.QUOTE_MINIMAL)    
        spamwriter.writerow(header)
        index=0
        enddata=keithley.query(':TRACe:ACTual:END? "buffer3"')
        print "Total data counts: %s"%enddata
        print "Saving data to %s"%result_csv
        initial=1
        for count in range(1000000,int(enddata)+1,1000000):
            print "Print data from %d to %d"%(initial,count)
            voltage = keithley.query_ascii_values(':TRACe:DATA? '+str(initial)+', '+str(count)+',"buffer3", READ, REL')
            initial=count+1
            number =0
            data=[]
            for item in voltage:                            
                if (number %2) == 0 and len(data)>0:           
                    #print "%d\t%s\t%s\t"%(index,data[0],data[1]) 
                    spamwriter.writerow(data)        
                    index = index+1
                    data=[]
                    data.append(item)
                else:
                    data.append(item)
                number = number+1
    except KeyboardInterrupt:
        print "Interrupt happened. Close program gracefully."
        keithley.close()
        Result_file.close()        
    finally:
        print "Data processing compeleted!"
        keithley.close()
        Result_file.close()

def dmm7510_dmm_loger_stream_current(result_folder="C:\Temp\data.csv",samplerate='1000000',port='USB0::0x05E6::0x7510::04353687::INSTR'):

    result_csv = result_folder      
    rm = visa.ResourceManager()
    print rm.list_resources()
    keithley = rm.open_resource(port)
    #Reset the instrument
    keithley.write('*RST')
    #Set the measurement function to Digitize Voltage to capture the power-up behavior
    keithley.write(':SENSe:DIGitize:FUNCtion "CURR"')
    #Current range must be fixed when using Digitizing Voltage
    keithley.write(':DIG:CURR:RANG 1')
    #Set the display resolution to the minimum - really only care about what's in the buffer
    keithley.write(':DISP:DIGitize:CURRent:DIG 3')
 
    #Set the sample rate to 1MHz to capture any glitch
    capture_rate=':SENSe:DIGitize:CURRent:SRATe '+samplerate
    keithley.write(capture_rate)
    #Set aperture to auto to get the highest accuracy measurement for the sampling rate configured
    keithley.write(':SENSe:DIGitize:CURRent:APERture AUTO')
    keithley.write(':TRACe:FILL:MODE CONT, "defbuffer1"')
    #Clear buffer
    keithley.write(':TRACe:CLEar "defbuffer1"')
    header= ["Reading","Time"]
    Result_file = open(result_csv,'wb') 
    spamwriter = csv.writer(Result_file,dialect='excel',quoting=csv.QUOTE_MINIMAL)    
    spamwriter.writerow(header)
    index=0
    print "Saving data to %s"%result_csv
    try:
        while True:
            voltage = keithley.query_ascii_values(':MEASure:DIGitize:CURRent? "defbuffer1", READ, REL')        
            #initial=count+1
            #number =0
            data=[]
            spamwriter.writerow(voltage)
    except KeyboardInterrupt:
        print "Keyboard Interrupt Happened"
        keithley.close()
        Result_file.close()            
        pass
    finally:
        print "Data processing compeleted!"
        keithley.close()
        Result_file.close()            
    
def dmm7510_dmm_loger_stream_voltage(result_folder='C:\Temp\data.csv',samplerate='1000000',port='USB0::0x05E6::0x7510::04353687::INSTR'):

    result_csv = result_folder     
    rm = visa.ResourceManager()
    print rm.list_resources()
    keithley = rm.open_resource(port)
    #Reset the instrument
    keithley.write('*RST')
    #Set the measurement function to Digitize Voltage to capture the power-up behavior
    keithley.write(':SENSe:DIGitize:FUNCtion "VOLT"')
    #Current range must be fixed when using Digitizing Voltage
    keithley.write(':DIG:VOLT:RANG 10')
    #Set the display resolution to the minimum - really only care about what's in the buffer
    keithley.write(':DISP:DIGitize:VOLT:DIG 3')
    keithley.write(':DIG:VOLT:INP AUTO')
    #Set the sample rate to 1MHz to capture any glitch
    capture_rate=':SENSe:DIGitize:VOLT:SRATe '+samplerate
    keithley.write(capture_rate)
    #Set aperture to auto to get the highest accuracy measurement for the sampling rate configured
    keithley.write(':SENSe:DIGitize:VOLT:APERture AUTO')
    keithley.write(':TRACe:FILL:MODE CONT, "defbuffer1"')
    #Clear buffer
    keithley.write(':TRACe:CLEar "defbuffer1"')
    header= ["Reading","Time"]
    Result_file = open(result_csv,'wb') 
    spamwriter = csv.writer(Result_file,dialect='excel',quoting=csv.QUOTE_MINIMAL)    
    spamwriter.writerow(header)
    index=0
    print "Saving data to %s"%result_csv
    try:
        while True:
            voltage = keithley.query_ascii_values(':MEASure:DIGitize:CURRent? "defbuffer1", READ, REL')        
            #initial=count+1
            #number =0
            data=[]
            spamwriter.writerow(voltage)
    except KeyboardInterrupt:
        print "Keyboard Interrupt Happened"
        print "Data processing compeleted!"
        keithley.close()
        Result_file.close()
        pass
    finally:
        print "Data processing compeleted!"
        keithley.close()
        Result_file.close()         
 
def main(argv=None):
    '''
    Expecting the argument to be entered as :
    function, protocal, resultpath, samplerate, numberofsamples
    EX:
       python dmm_v2.py currcont USB0::0x05E6::0x7510::04353687::INSTR C:\Temp\data.csv 1000000 10000000
    function options: 
    currcont = continoustly measure current 
    currbuff = measure current in the buffer
    voltcont = continoustly measure voltage 
    voltbuff = measure voltage in the buffer    
    '''
    try:
        numofsamples='10000000'
        result_folder="C:\Temp\data.csv"
        samplerate='1000000'
        portid='TCPIP0::192.168.1.180::inst0::INSTR'
        if argv is None:
            argv = sys.argv
        try:
            print "Entering %s function"%argv[1]
            function = argv[1]
        except:
            print "No function value given!"
        try:
            print "Port:%s "%argv[2]
            portid = argv[2]
        except:
            print "No port given use default port :%s"%portid 
            #portid = 'USB0::0x05E6::0x7510::04353687::INSTR'       
        try:
            print "Result folder %s "%argv[3]
            path = argv[3]
        except:
            print "No path value given! Use default path %s"%result_folder 
            path = result_folder
        try:
            print "Sample Rate %s "%argv[4]
            sample = argv[4]
        except:
            print "No path value given! Use default path %s"%samplerate 
            sample = samplerate  
        try:
            print "Number of sample collected %s "%argv[5]
            nsample = argv[5]
        except:
            print "No path value given! Use default path %s"%numofsamples
            nsample = numofsamples         
        if function == 'currcont':
            dmm7510_dmm_loger_stream_current(result_folder=path,samplerate=sample,port=portid)
        elif function == 'voltcont':
            dmm7510_dmm_loger_stream_voltage(result_folder=path,samplerate=sample,port=portid)
        elif function == 'currbuff':
            dmm7510_dmm_loger_current(numofsamples=nsample,result_folder=path,samplerate=sample,port=portid)
        elif function == 'voltbuff':
            dmm7510_dmm_loger_voltage(numofsamples=nsample,result_folder=path,samplerate=sample,port=portid)        
    except Exception as e:
        print str(e)

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print str(e)    

