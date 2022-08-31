import pyvisa
import time

class dmm6500:
    dmmResourceName = ''
    dmmResource = ''
    rm = ''
    timeout = 0

    def __init__(self, timeout):
        self.timeout = timeout
        self.rm = pyvisa.ResourceManager()
        list = self.rm.list_resources()
        print(list)
        self.dmmResourceName = list[0]

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self):
        self.dmmResource.close()
    
    def open(self):
        self.dmmResource = self.rm.open_resource(self.dmmResourceName)
        self.dmmResource.timeout = self.timeout

    def close(self):
        self.dmmResource.close()
    
    def setVoltageDC(self, range = 'auto', autzoero=False, nplc=1, aver = False, tcon='off', count = 1):
        Volt_rangelist = ['auto', 0.1, 1, 10, 100, 1000]
        if range not in Volt_rangelist:
            raise ValueError('not supported in range')
        if nplc < 1 or nplc > 12:
            raise ValueError('NPLC has to be between 1 and 12')
        if autzoero:
            autozero = 'ON'
        else:
            autozero = 'OFF'
        if aver:
            if tcon != 'REP' and tcon != 'MOV':
                raise ValueError('TCON value has to be off, REP or MOV')
            aver = f'; :SENS:VOLT:AVER:TCON {tcon}; :SENS:VOLT:AVER:COUN {count}; :SENS:VOLT:AVER:STAT ON'
        else:
            aver = ''

        if range == 'auto':
            range = ':AUTO ON'
        else:
            range = f' {range}'
        
        query = f'*RST; :SENS:FUNC "VOLT:DC"; :SENS:VOLT:RANG{range}; :SENS:VOLT:NPLC {nplc}; :SENS:VOLT:AZER {autozero}; {aver}'
        print(query)
        self.dmmResource.write(query)

    def setCurrentDC(self, range = 'auto', autzoero=False, nplc=1, aver = False, tcon='off', count = 1):
        Curr_rangelist = ['auto', 10e-6, 100e-6, 1e-3, 0.01, 0.1, 1, 3]
        if range not in Curr_rangelist:
            raise ValueError('not supported in range')
        if nplc < 1 or nplc > 12:
            raise ValueError('NPLC has to be between 1 and 12')
        if autzoero:
            autozero = 'ON'
        else:
            autozero = 'OFF'
        if aver:
            if tcon != 'REP' and tcon != 'MOV':
                raise ValueError('TCON value has to be off, REP or MOV')
            aver = f'; :SENS:CURR:AVER:TCON {tcon}; :SENS:CURR:AVER:COUN {count}; :SENS:CURR:AVER:STAT ON'
        else:
            aver = ''

        if range == 'auto':
            range = ':AUTO ON'
        else:
            range = f' {range}'
        
        query = f'*RST; :SENS:FUNC "CURR:DC"; :SENS:CURR:RANG{range}; :SENS:CURR:NPLC {nplc}; :SENS:CURR:AZER {autozero}; {aver}'
        print(query)
        self.dmmResource.write(query)
        pass

    def set4WResistance(self, range = 'auto', autzoero=False, nplc=1, aver = False, tcon='off', count = 1):
        Res_rangelist = ['auto', 1, 10, 100, 1000, 10e3, 100e3, 1e6, 10e6, 100e6]
        if range not in Res_rangelist:
            raise ValueError('not supported in range')
        if nplc < 1 or nplc > 12:
            raise ValueError('NPLC has to be between 1 and 12')
        if autzoero:
            autozero = 'ON'
        else:
            autozero = 'OFF'
        if aver:
            if tcon != 'REP' and tcon != 'MOV':
                raise ValueError('TCON value has to be off, REP or MOV')
            aver = f'; :SENS:FRES:AVER:TCON {tcon}; :SENS:FRES:AVER:COUN {count}; :SENS:FRES:AVER:STAT ON'
        else:
            aver = ''

        if range == 'auto':
            range = ':AUTO ON'
        else:
            range = f' {range}'
        
        query = f'*RST; :SENS:FUNC "FRES"; :SENS:FRES:RANG{range}; :SENS:FRES:NPLC {nplc}; :SENS:FRES:AZER {autozero}; {aver}'
        print(query)
        self.dmmResource.write(query)
        pass    

    def read(self):
        return self.dmmResource.query(':READ?')

    def getId(self):
        return self.dmmResource.query('*IDN?')

    def reset(self):
        self.dmmResource.write('*RST')

# def CodiceProva():
#     #Misura la corrente, switchando setting automaticamente
#     print(dmm.query('MEAS:CURR?'))
#     #Misura la tensione
#     print(dmm.query('MEAS:VOLT?'))
#     #Misura di tensione un po' più spinta
#     query = '*RST; :SENS:FUNC "VOLT:DC"; :SENS:VOLT:RANG 10; :SENS:VOLT:INP AUTO; :SENS:VOLT:NPLC 12; :READ?'
#     print(dmm.query(query))
#     #Resistenza a 4 fili
#     query = '*RST; :SENS:FUNC "FRES"; :SENS:FRES:RANG:AUTO ON; :SENS:FRES:OCOM ON; :SENS:FRES:AZER ON; :SENS:FRES:NPLC 1; :READ?'
#     #Misura di corrente più spinta
#     query = '*RST; :SENS:FUNC "CURR:DC"; :SENS:CURR:RANG:AUTO ON; :SENS:CURR:NPLC 12; :READ?'
#     #Se uno vuole fare delle medie  deve fare 
#     query = '*RST; :SENS:FUNC "CURR:DC"; :SENS:CURR:RANG:AUTO ON; :SENS:CURR:NPLC 12; :SENS:CURR:AZER ON; :SENS:CURR:AVER:TCON REP; :SENS:CURR:AVER:COUN 10 ; :SENS:CURR:AVER:STAT ON'
#     #e poi piano piano chiedere la lettura
#     #Resistenza a 4 contatti con medie e quant'altro
#     query = '*RST; :SENS:FUNC "FRES"; :SENS:FRES:RANG:AUTO ON; :SENS:FRES:NPLC 12; :SENS:FRES:OCOM ON; :SENS:FRES:AZER ON; :SENS:FRES:AVER:TCON REP; :SENS:FRES:AVER:COUN 10 ; :SENS:FRES:AVER:STAT ON' 
#     pass

if __name__ == '__main__':
    with dmm6500(100) as dmm:
        while(True):
            dmm.setVoltageDC()
            time.sleep(1)
            print(dmm.read())
