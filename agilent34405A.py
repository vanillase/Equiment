#-------------------------------------------------------------------------------
# Name:        agilent34495A
# Purpose:     Control agilent34495A DMM Single Measure resistance . 
#           
# Author:      li.chelsey@gmail.com
#
# Created:     31/12/2017
# Copyright:   (c) li.chelsey@gmail.com
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import visa

def agilent34405A():
    rm = visa.ResourceManager('@py')
    resources = rm.list_resources()
    print "Resources:%s"%resources
    inst = rm.open_resource('USB0::2391::1560::TW47510072::0::INSTR')
    inst.write('*RST')
    inst.write('*IDN?')
    #machine = inst.read()
    #print machine
    #inst.write(':INITiate:IMMediate')
    #inst.write(':FORMat:DATA ASCii')
    inst.write(':SENSe:RES:RANGe:AUTO')
    inst.write(':SENSe:RES:RES:AUTO')
    #inst.write(':MEASure:RES?')
    inst.write(':MEASure:RESistance?')
    #inst.write("DATA:DATA? NVMEM")
    
    #inst.write(':DATA:POINts? ')
    #result = inst.query(":FETCh?")
    #inst.write(":READ?")
    #reasult = inst.read()
    result = inst.read()
    print "Resistance:%s"%result 
    inst.close()


agilent34405A()
