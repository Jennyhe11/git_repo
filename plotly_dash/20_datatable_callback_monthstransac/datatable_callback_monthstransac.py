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

@app.callback(
    Output('datatable','style_data_conditional'),
    Output('datatable','style_cell'),
    Output('datatable','style_data'),
    Output('datatable','style_header'),
    Output('datatable','style_table'),
    Input('datatable','data')
)

def style_table(data):
    df_style = pd.DataFrame.from_dict(data)
    df_style.index = df_style['Product']
    df_style.drop(columns = ['Product'],inplace = True)

    df_numeric_columns = df_style.select_dtypes('number')
    
    style_data_conditional=(
        [
                {
                    'if': {
                        'filter_query': '{{{}}} > 1000'.format(col),
                        'column_id': col ,
                    },
                    'backgroundColor': '#7FDBFF',
                    'color': 'white'
                } for col in df_numeric_columns.columns
            ]+
            [
              {
                    'if': {
                        'filter_query': '{{{}}} > 2000'.format(col),
                        'column_id': col ,
                    },
                    'backgroundColor': '#FF4136',
                    'color': 'white'
                } for col in df_numeric_columns.columns  
            ]
    )
   
    style_cell={                
            'minWidth': 95, 'maxWidth': 95, 'width': 95,'padding': '5px','font-family':'sans-serif'
        }

    style_data={                
            'whiteSpace': 'normal',
            'height': 'auto'
        }

    style_header={
         'backgroundColor': 'gray',
         'fontWeight': 'bold',
         'border': '1px solid black'
     }

    style_table={'height': '400px','width':'1000px','overflowY': 'auto'}

    return style_data_conditional,style_cell, style_data, style_header, style_table

if __name__ == '__main__':
    app.run_server()
