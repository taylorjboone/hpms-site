import pandas as pd
from io import StringIO
rowdict = {'REC_ORG': (0, 7),
 'ACT': (7, 11),
 'HOME_ORG': (11, 16),
 'DOC_NO': (16, 28),
 'REPT_DATE': (28, 37),
 'AUTH': (37, 45),
 'N_P': (45, 47),
 'ROUTE_NO': (47, 57),
 'BMP': (57, 64),
 'EMP': (64, 71),
 'ACCOMP': (71, 80),
 'MEAS_ENTERED': (80, 88),
 'ACT_MEASURED': (88, 94),
 'REC_TYPE': (94, 99),
 'ACCT': (99, 104),
 'UNITS': (104, 114),
 'AMOUNT': (114, 124),
 'MEAS_ERR': (124, 128)}


# output file is an xlsx file 
def rpt_converter(inputfile,outputfile):
    # outfn = open(outputfile,'w')
    data = open(inputfile,'r').read()
    header = 'Org Number,Activity,Org,Doc Number,Date,Authorization,N/P,Route Number,BMP,EMP,Accomplished,Measure Entered,Activity Measured,Type Number,Account,Unit,Amount Text,Measure Error'
    header2 = 'REC_ORG,ACT,HOME_ORG,DOC_NO,REPT_DATE,AUTH,N_P,ROUTE_NO,BMP,EMP,ACCOMP,MEAS_ENTERED,ACT_MEASURED,REC_TYPE,ACCT,Unit,Amount Text,MEAS_ERR'
    # header.write(header)
    newlist = [header]
    for row in data.splitlines():
        striprow = row.strip()
        beg = striprow[:13].strip()
        if check_beg(beg):
            row = [get_column(k,v,row) for k,v in rowdict.items()]
            newlist.append(','.join(row))
    data = pd.read_csv(StringIO('\n'.join(newlist)))
    data['Amount Text'].loc[data['Amount Text'].isna()] = 0
    data['Unit'].loc[data['Unit'].isna()] = 0
    data['isjv'] = 'no'
    data['isjv'].loc[data['Amount Text'].str.contains('-', na=False)] = 'yes'
    data['Amount Text'].loc[data['isjv'] == 'yes']=data['Amount Text'].loc[data['isjv'] == 'yes'].map(lambda x : (x.replace('-','')))
    data['Amount Text'].loc[data['isjv'] == 'yes']=data['Amount Text'].loc[data['isjv'] == 'yes'].map(lambda x : ('-' + x))
    
    # data['Amount Text'].loc[data['isjv'] == 'yes'].map(lambda x: '-' + x)
    
    # data['Amount Text'].loc[data['Amount Text'].str.contains('-',na=False)].map(lambda x: '-' + x.split('-'))

    # data['Amount Text'] = data['Amount Text'].replace('\-','',regex=True)
    data['Amount Text'] = data['Amount Text'].replace('\,','',regex=True)
    # data['Amount Text'] = data['Amount Text'].astype('float64')
    # data.to_excel(outputfile,index=False)
    
    data=data.drop(columns='isjv')
    with pd.ExcelWriter(outputfile,
                    engine = 'xlsxwriter',
                    options = {'strings_to_numbers': True}) as outputfile:
                    data.to_excel(outputfile,index=False)

    
    return outputfile

    # return data


# checks the beginning of the row
def check_beg(beg):
    beg = str(beg).split(' ')
    if len(beg) == 3:
        boolval = True 
        for i in beg:
            if not i.isdigit():
                boolval = False 
        return boolval 
    else:
        return False 


# gets a columns 
def get_column(k,v,row):
    id1,id2 = v 
    return '"%s"' % row[id1:id2].strip()


