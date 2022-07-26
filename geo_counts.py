import pandas as pd
from os import listdir
from os.path import isfile, join
import os



mypath='C:\PythonTest\Voltron\district_chrystal_report_website\hpms-site\geo_count_home_folder'
number=1
# geo=pd.read_csv('C:/PythonTest/Voltron/district_chrystal_report_website/hpms-site/013001_202109210000_0 (1).txt',skiprows=16,sep=';',header=None)




def metro_count_convert(in_filename,out_filename='default.xlsx'):
    z=pd.read_csv(in_filename,skiprows=16,header=None)
    # print(z,z.columns,z[1].str.split(',',expand=True))
    z[['-a','Date']]=z[0].str.split(';',expand=True)
    z[['time']]=z[1]
    z[['channel','Speed']]=z[2].str.split(';',expand=True)
    z[['VClass']]=z[3]
    z[['Number of Axels']]=z[4]
    z[['Wheel Base']]=z[5]
    z[['Quality Control']]=z[6]
    z=z.drop([0,1,2,3,4,5,6,'-a'],axis=1)
    return z.to_excel(out_filename,index=False)

def centurion_count_convert(in_filename,out_filename='default.xlsx'):
    z=pd.read_csv(in_filename,skiprows=22,header=None)
    z[['-a','Date']]=z[0].str.split(';',expand=True)
    z[['Time']]=z[1]
    z[['Channel','Speed']]=z[2].str.split(';',expand=True)
    z[['Naxles']]=z[3]
    z[['Length']]=z[4]
    z[['Vclass']]=z[5]
    z[['Vclass1','i','Axle Length 1','Axle Length 2','Axle Length 3','Axle Length 4','Axle Length 5','Axle length 6','Axle Length 7']]=z[6].str.split(';',expand=True)
    z=z.drop(['-a',0,1,2,3,4,5,6],axis=1)
    return z.to_excel(out_filename,index=False)


onlyfiles = [os.path.join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f)) if f.endswith('.txt')]
term1='MetroCount'
term2='Centurion-'
cent_number=1
metro_number=1
for a in onlyfiles:
    file=open(a).read().splitlines()
    is_cent = 'Centurion' in file[3] and 'FV' in file[3]
    is_metro = 'MetroCount' in file[3] and 'FV' in file[3]
    if is_cent==True:
        new_name=r'C:\PythonTest\Voltron\district_chrystal_report_website\hpms-site\centurion_count\centurion_%d.xlsx' % cent_number
        cent_number+=1
        centurion_count_convert(a,out_filename=new_name)
    if is_metro==True:
        new_name=r'C:\PythonTest\Voltron\district_chrystal_report_website\hpms-site\metro_count\metro_%d.xlsx' % metro_number
        metro_number=+1
        metro_count_convert(a,out_filename=new_name)

    # for line in file:
    #     # line.strip().split('-')
    #     if term1 in line:
    #         print(line,a)
    #         metro_count_convert(a)
    #     if term2 in line:
    #         print(line,a)
    #         centurion_count_convert(a)
        # else:
        #     print('Not a known GEOCOUNT File')

# metro_count_convert(mypath)