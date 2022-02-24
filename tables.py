from dash import dash_table
from dash.dash_table.Format import Format, Scheme, Trim

table_index = 0

def make_datatable(df, dataset):
    global table_index
    table_index += 1

    return dash_table.DataTable(
        id={'type': 'datatable_table', 'dataset': dataset, 'index': table_index},
        columns=[
            (dict(name=i, id=i, hideable=False, type='numeric',
                  format=Format(precision=4, scheme=Scheme.fixed, trim=Trim.yes))
             if i != 'Species' else
             dict(name=i, id=i))
            # {"name": i, "id": i, "hideable": True}
            for i in df.columns
            if i not in ['numIndex', 'id']

        ],
        data=df.to_dict('records'),  # the contents of the table
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        # column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",  # allow users to select 'multi' or 'single' rows
        # row_deletable=True,  # choose if user can delete a row (True) or not (False)
        page_size=8,  # number of rows visible per page
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            #        'minWidth': 95, 'maxWidth': 95, 'width': 95,
            'fontSize': 12, 'font-family': 'sans-serif'

        },
        style_data={  # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'}

    )
