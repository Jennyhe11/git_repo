import pandas as pd
from dash import Dash,dcc,html,Input,Output,dash_table

df = pd.read_excel("Asin_Report.xlsx",index_col = 'month')
df['Year'] = df.index.year
df['Month'] = df.index.month

cols = ['Year','Month','Product','Sessions']
df = df[cols]
df = df.reset_index(drop=True)

# This is the dataFrame to be used in the first dash callback
df = df.pivot_table(index = ['Product'] ,columns = ['Year','Month'], values = 'Sessions')

#df.columns
#df.columns.get_level_values('Year')
#df.columns.get_level_values('Year').unique()
#df_data = df.xs(2021,level = 0,axis = 1)
# map_month = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
# df_data.columns = df_data.columns.map(map_month)
#df_data.reset_index()


app = Dash(__name__)

app.layout = html.Div([
    html.H4('This is an DataTable'),
    dash_table.DataTable(id = 'datatable'),
    dcc.Dropdown(id = 'dropdown', 
                 options = df.columns.get_level_values('Year').unique(), 
                 value = df.columns.get_level_values('Year').unique())
])

@app.callback(
    Output('datatable','data'),
    Input('dropdown','value')
)

def update_datatable(year):
    df_data = df.xs(year,level = 0, axis = 1)
    map_month = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    df_data.columns = df_data.columns.map(map_month)
    df_data = df_data.reset_index()
    
    return df_data.to_dict('records')

if __name__ == '__main__':
    app.run_server()
