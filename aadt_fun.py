import pandas as pd

old_df = pd.read_excel(r'G:\.shortcut-targets-by-id\1DY5tu5QknvUYX92CJdhJSjyAUZ7MYnsE\aadt_patrick\aadt_patrick.xlsx')
new_df = pd.read_excel(r'G:\.shortcut-targets-by-id\1DY5tu5QknvUYX92CJdhJSjyAUZ7MYnsE\aadt_patrick\new_bridge_mps.xlsx')

new_df['new_aadt'] = ''

def mapper(x):
    rid,mp = x['RouteID'], x['MilePoint']
    x['new_aadt'] = old_df['AADT'].loc[(old_df['FROM_MEASURE'] > mp > old_df['TO_MEASURE']) & (old_df['ROUTEID'] == new_df['RouteID'])]