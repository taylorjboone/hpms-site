import pandas as pd
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True
worksheet=pd.read_excel(r"C:\Users\e104200\Downloads\activity codes.xlsx", sheet_name=1)
my_dict={}


# for i in range(1, len(worksheet)):
#     row = worksheet.iloc[i]
#     my_dict[row[0]] = [row[1],row[2]]

# for k,v in my_dict.items():
#     print(k,v)

@app.route('/', methods=['GET'])
def dropdown():
    for i in range(1, len(worksheet)):
        row = worksheet.iloc[i]
        my_dict[row[0]] = [row[1],row[2]]

    for k,v in my_dict.items():
        print(k,v)

    return render_template('kortni.html',data=my_dict)

if __name__ == "__main__":
    app.run()








