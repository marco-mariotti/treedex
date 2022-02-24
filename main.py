### style scatterplot: white bkg, more visible points when unselected
#   table: toggle-column is ugly; have something to select all (visible only)?
#   fix ete id --> connected scatterplot, tree

######
# 20 12 21
##### Init: put df in dataframe_store and only there
# (expect for name2node mapping in memory somewhere)
# in sync_selection: for each object, understand dataset --> get corresponding df_records
## options empty? then default ones = first columns which is not species

### datatable and scatter
# update code to work with records instead of dataframe
# make_combo optional argument: dataset name
# if not provided: use empty plot

## put a second dataset for testing purposes

##
# simplify input df. Only species needed, no indexed as such: numeric index is all you need
# datatable: menu where dataset is selected

### Load file:
## head with load file --> click load
#  tail with:
# dataset title: '    '  compulsory, derived from filename
# hey! no Species column detected. Please choose it here:
# warning: X of Y Species could not be mapped


### 21 12 21
# it works.
# but filling default values won't work with current model because:
#  store.data calls dropdown fill
#  need button to resave store.data
#
## just put the procedure for finding defaults in update_scatter_options_store, it's called first
# to do this, need to get the input to get dataframe


# import os
import dash
import logging
from dash.dependencies import Input, Output, State, MATCH, ALL
# from dash import dash_table, dcc, html  #redundant
# import dash_bootstrap_components as dbc #redundant
# import plotly.express as px #redundant
from ete_component import EteComponent
import numpy as np
import pandas as pd

from tables import *
from plots import *
from utils import *
from treedexcolors import *

#from ete_link import treeid,  tree, id2node, node2id, name2node
import ete4
from ete4.smartview.gui.server import run_smartview
from werkzeug.serving import run_simple # werkzeug development server
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import redirect, url_for

import os
os.chdir('/Users/mmariotti/ete4/treedex')


dataframe_storage_type = 'local'

#  loading quantitative data
df = pd.read_csv("Lifehistory.csv")
df.rename(columns={'ML': 'MaxLifespan'}, inplace=True)
df['logAdultWeight'] = np.log10(df['AdultWeight'])
# df['SpeciesIndex'] = df['Species']
# df.set_index('SpeciesIndex', inplace=True)
# df['numIndex'] = [i for i in range(len(df))]
# df['id'] = df.index
df['id'] = [i for i in range(len(df))]

app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])
dash_server = app.server
ete_path = "/ete"
ete_url = "http://localhost:5001" + ete_path



tree = ete4.Tree('mammal_tree.nw')
# id2node   = {n.id: n for n in tree.traverse()}
## inefficient and ugly
id2node = {}
node2id = {}
name2node = {}

def get_node_id(tree, node, node_id):
    parent = node.up
    if not parent:
        node_id.reverse()
        return node_id
    node_id.append(parent.children.index(node))
    return get_node_id(tree, parent, node_id)

for n in tree.traverse():
    theid = ",".join(map(str, get_node_id(tree, n, [])))
    id2node[theid] = n
    node2id[n] = theid
    name2node[n.name] = n





#tree= ete4.Tree("(((a:1,b:1):1,c:1):1, ((e:1, f:1), g:1):1);") # custom tree

ete_app = run_smartview(tree=tree, tree_name="treedex", run=False, safe_mode=True)
ete_app.logger.disabled = True
logging.getLogger('werkzeug').disabled = True

# we need to add ETE's static to Dash app (only root app serves static files)
@dash_server.route(ete_path)
def index():
    return redirect(url_for("static", filename='gui.html', tree=tree))


# GLOBAL APP
application = DispatcherMiddleware(app.server, { ete_path : ete_app })


ete_iframe = EteComponent({'type': 'ete_iframe', 'index': 1, 'dataset': 'None'},
                          #id='ete_iframe',
                          url=ete_url,
                          path=ete_path,
                          treeid=0,
                          # height="800px",
                          # width="500px"
                          )

# -------------------------------------------------------------------------------------
# App layout

app.layout = html.Div(
    dbc.Col([dbc.Row(dbc.Col(html.H4('Treedex prototype: linking dash and ete4'), class_name='text-center')),
             dbc.Row(
                 [dbc.Col(ete_iframe, width=5, class_name="border border-primary g-0"),
                  dbc.Col([
                      dbc.Row(make_datatable(df, 'Lifehistories'),
                              class_name="border border-primary g-0"),
                      make_scatter_combo('Lifehistories', df.to_dict('records'))  ####

                  ], class_name="g-0", width=7),
                  ], class_name="g-0"),

             dbc.Row([
                 # dbc.Col(dcc.Graph(id='scatter3d1_gra'), width=6, class_name="border border-primary"),
                 # dbc.Col(dcc.Graph(id='bar1_gra', config=bar_config), width=6, class_name="border border-primary")
             ]),
             # dbc.Row(dbc.Col(
             #     dbc.Button("Clear data stored", size="sm", n_clicks=0,
             #                id='clear_data_button'))),

             dbc.Row(dbc.Col(dbc.Alert("This is an info alert. Good to know!",
                                       id='message_board', color="info"))),

             # dcc.Store(id='dataframe_store',
             #           storage_type=dataframe_storage_type,
             #           data={'Lifehistory': df.to_dict('records')})

             #
             # html.Button('Click me!', id='button_show_message', n_clicks=0),
             # html.Div(id='message_board'),
             dbc.Row(dbc.Col(dbc.Alert("This is an info alert. Good to know!",
                                       id='message_board2', color="alert"))),
             # html.Button('Select a specific node', id='button_do_something'),
             #
             # html.Button('Force echo activeLeaves', id='button_echo_ete'),

             ]))


# @app.callback(
#      Output('message_board', 'children'),
#      Input({'type': 'ete_iframe', 'dataset': ALL, 'index': ALL}, 'activeLeaves')
# )
# def echo(ete_active_list):
#     return str(ete_active_list[0])


# @app.callback(
#      Output('message_board2', 'children'),
#      Input('button_echo_ete', 'n_clicks'),
#      State({'type': 'ete_iframe', 'dataset': ALL, 'index': ALL}, 'activeLeaves')
# )
# def echo(n_clicks, ete_active_list):
#     if not n_clicks:
#         return dash.no_update
#     return str(ete_active_list[0])
#

# @app.callback(
#     Output( {'type': 'ete_iframe', 'dataset': ALL, 'index': ALL}, 'activeLeaves'),
#     Input('button_do_something', 'n_clicks')
# )
# def pressed_button(n_clicks):
#     if not n_clicks:
#         return dash.no_update
#     # return [ [ #{'id':'1,1,1,1,1,1,0,1,0,1,1,0'}] ]
#     # ]]
#     #
#     #return [[{'name': 'Cavia_porcellus', 'dist': 0.0393987, 'support': 1, 'id': '1,1,1,1,1,1,1,0,0'}, {'name': 'Heterocephalus_glaber', 'dist': 0.0209233, 'support': 1, 'id': '1,1,1,1,1,1,1,0,1,0'}, {'name': 'Fukomys_damarensis', 'dist': 0.0233638, 'support': 1, 'id': '1,1,1,1,1,1,1,0,1,1'}]
#     return [[{'id': '1,1,1,1,1,1,1,0,0'},
#              {'id': '1,1,1,1,1,1,1,0,1,0'},
#              ]
# ]



#######################################################################################################################
@app.callback(
    [Output('message_board', 'children'),
     Output({'type': 'scatter_graph', 'dataset': ALL, 'index': ALL}, 'figure'),
     Output({'type': 'ete_iframe', 'dataset': ALL, 'index': ALL}, 'activeLeaves'),
     Output({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'selected_rows')
     ],

    [Input({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'selected_rows'),
     Input({'type': 'scatter_graph', 'dataset': ALL, 'index': ALL}, 'selectedData'),  # selection
     Input({'type': 'scatter_store', 'dataset': ALL, 'index': ALL}, 'data'),  # options
     Input({'type': 'ete_iframe', 'dataset': ALL, 'index': ALL}, 'activeLeaves'),  # selection#
     ],

    [State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'data'),
     State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'id'),
     State({'type': 'scatter_store', 'dataset': ALL, 'index': ALL}, 'id')]
)

def sync_selection(tbl_selected_rows_list,
                   sca_selected_data_list,
                   sca_options_list,
                   ete_activeleaves_list,

                   table_datasets,  # state, carries the dataframes in record forms
                   table_ids,
                   sca_options_ids,  # state
                   ):
    # print( dash.callback_context.triggered[0]['prop_id'].split('.') )

    ## getting links to dataframe records
    dataset2records = {tab_id['dataset']: table_datasets[i] for i, tab_id in enumerate(table_ids)}

    # new shape of ete_active_list: {'nodes': [], 'clades': []}


    ## ete keeps ancestral nodes selected, thus I must read its selecrtion in any case:
    ete_selected_species = []
    ete_selected_ancestors = []
    if ete_activeleaves_list[0]:  ## assuming a single ETE instance
        for dic in ete_activeleaves_list[0]:
            #print( ('%% selected node = ', i) )
            node = id2node[dic['id']]
            #if node.is_leaf():
            ete_selected_species.append(node.name)
            # else:
            #     ete_selected_ancestors.append(node)
            #     ete_selected_species.extend([leaf.name for leaf in node])

    ### determining new species selection
    # which of the inputs were triggered?

    ## so ugly, jeez I hope they improve this in later plotly/dash versions:
    fired_dataset, fired_index, fired_type, fired_prop = who_fired()
    print(('Fired sync_selection: ', fired_dataset, fired_index, fired_type, fired_prop))

    print(('sca_len', len(sca_selected_data_list), len(sca_options_ids), len(sca_options_list)))
    print(('sca_options: ', sca_options_ids, sca_options_list))

    ## If multiple tables or multiple scatterplots are here, how does sca_selected_data_list look like?
    ## left to do!!!
    tbl_selected_rows = tbl_selected_rows_list[0] if tbl_selected_rows_list else []
    sca_selected_data = sca_selected_data_list[0] if sca_selected_data_list else []

    if fired_type == 'datatable_table':
        tbl_selected_rows_species = [dataset2records[fired_dataset][i]['Species'] for i in tbl_selected_rows]
        selected_species = tbl_selected_rows_species

    elif fired_type == 'scatter_graph':
        sca_selected_species = ([dataset2records[fired_dataset][p['pointIndex']]['Species']
                                 for p in sca_selected_data['points']]
                                if sca_selected_data else [])
        selected_species = sca_selected_species

    elif fired_type == 'ete_iframe':
        selected_species = ete_selected_species

    elif fired_type == 'scatter_store':
        # selection didn't change; some options did. using ete to fetch currently selected species
        selected_species = ete_selected_species

    else:
        selected_species = []

    if any([not o for o in sca_options_list]):
        print('empty options scatter store callback --> no update ')
        return dash.no_update

    ### preparing data for the various objects to update their selection
    # selected_indices = df['numIndex'][df['Species'].isin(set(selected_species))]
    sel_sp_set = set(selected_species)
    datasets_displayed = set([sca_id['dataset'] for sca_id in sca_options_ids] +
                             [tab_id['dataset'] for tab_id in table_ids])
    dataset2selected_indices = {dataset: [i for i, row in enumerate(dataset2records[dataset])
                                          if row['Species'] in sel_sp_set]
                                for dataset in datasets_displayed}

    # out_tbl=selected_indices
    out_ete = ([{'id': node2id[name2node[s]]} for s in selected_species])

    # for i, sca_id in enumerate(sca_options_ids):        print(sca_options_list[i])

    # print('%%%%')
    # print( f"{type(dataset2records[sca_id['dataset']])}"  )
    # print( f"{dataset2records[sca_id['dataset']][0]}"  )
    # print( f"{dataset2records[sca_id['dataset']][0].keys()}"  )
    # print(f"{ list( dataset2records[sca_id['dataset']][0] ) [0]  }")

    return (  # to message board:
        [dbc.Row(f'dash.callback_context.triggered: {dash.callback_context.triggered}'),
         dbc.Row(f'ete_active:{ete_activeleaves_list[0]}'),
         dbc.Row(f'selected_species:{selected_species}'),
         # dbc.Row(f'tbl_selected_rows: {tbl_selected_rows}'),
         # dbc.Row(f'selected_indices: {selected_indices}'),
         ],

        [make_scatter_plot(dfr=dataset2records[sca_id['dataset']],
                           # first column
                           x=(sca_options_list[i]['x']
                               # if sca_options_list[i] else
                               # 'FTM'
                               # [k for k, v in dataset2records[sca_id['dataset']][0].items() if type(v) in (int, float)][0]
                               ),
                           # second column or first if missing
                           y=(sca_options_list[i]['y']
                               # if sca_options_list[i] else
                               # 'FTM'
                               # [k for k, v in dataset2records[sca_id['dataset']][0].items() if type(v) in (int, float)][0]
                               ),
                           # dataset2records[sca_id['dataset']][0].keys()[:2][-1]),
                           title=(sca_options_list[i]['title']
                               # if sca_options_list[i] else ''
                               ),
                           selection=dataset2selected_indices[sca_id['dataset']])

         for i, sca_id in enumerate(sca_options_ids)],

        # make_scatter3d(x='logAdultWeight', y='MaxLifespan', z='FTM', selection=selected_indices),
        # make_barplot(x='Species', y='MaxLifespan', selection=selected_indices),

        [out_ete],
        [dataset2selected_indices[tab_id['dataset']] for tab_id in table_ids]
    )
    # table


## add callback to syncronize ids with dropdown value
#


########################################################################################################################
@app.callback(
    Output({'type': 'scatter_store', 'dataset': ALL, 'index': MATCH}, 'data'),
    Input({'type': 'scatter_configure_ok', 'index': MATCH}, 'n_clicks'),
    [State({'type': 'scatter_dropdown', 'property': ALL, 'index': MATCH}, 'id'),
     State({'type': 'scatter_dropdown', 'property': ALL, 'index': MATCH}, 'value'),
     State({'type': 'scatter_inputtext', 'property': ALL, 'index': MATCH}, 'id'),
     State({'type': 'scatter_inputtext', 'property': ALL, 'index': MATCH}, 'value'),
     State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'data'),
     State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'id'),

     ])
def update_scatter_options_store(scatter_configure_ok_nclicks,
                                 dropdown_state_ids,
                                 dropdown_state_values,
                                 inputtext_state_ids,
                                 inputtext_state_values,
                                 table_datasets,  # state, carries the dataframes in record forms
                                 table_ids
                                 ):
    print('$$ update_scatter_options_store ')
    print(('IDS', dropdown_state_ids))
    print(('VALUES', dropdown_state_values))
    print(dash.callback_context.triggered)



    dataset2records = {tab_id['dataset']: table_datasets[i] for i, tab_id in enumerate(table_ids)}


    target_dataset =  [dropdown_state_values[i]   for i, dropdown_state_id in enumerate(dropdown_state_ids)
                         if dropdown_state_id['property']=='dataset'][0]

    if target_dataset is None:
        target_dataset = sorted(list(dataset2records))[0]

    numeric_cols = [k for k, v in dataset2records[target_dataset][0].items() if type(v) in (int, float)]
    state_out = {}
    numeric_defaults_used=0
    for i, dropdown_state_id in enumerate(dropdown_state_ids):
        if   dropdown_state_id['property'] == 'dataset':
            value = target_dataset   #default value set above
        elif dropdown_state_values[i] is None:
            value = (numeric_cols[numeric_defaults_used]
                     if len(numeric_cols) > numeric_defaults_used
                     else numeric_cols[-1])
            numeric_defaults_used += 1
        else:
            value = dropdown_state_values[i]
        state_out[dropdown_state_id['property']] = value

    for i, inputtext_state_id in enumerate(inputtext_state_ids):
        #value = inputtext_state_values[i]
        state_out[inputtext_state_id['property']] = (inputtext_state_values[i]
            if not inputtext_state_values[i]  is None else '')
        #state_out.update({inputtext_state_id['property']: inputtext_state_values[i]
        #              for i, inputtext_state_id in enumerate(inputtext_state_ids)})

    print(('state_out', state_out))
    print('^^ end update_scatter_options_store')

    return [state_out]


########################################################################################################################
@app.callback(
    [  # Output({'type': 'scatter_dropdown', 'property': ALL, 'index': MATCH}, 'id'),
        Output({'type': 'scatter_dropdown', 'property': ALL, 'index': MATCH}, 'options'),
        Output({'type': 'scatter_dropdown', 'property': ALL, 'index': MATCH}, 'value'),
        # Output({'type': 'scatter_inputtext', 'property': ALL, 'index': MATCH}, 'id'),
        Output({'type': 'scatter_inputtext', 'property': ALL, 'index': MATCH}, 'value'),
    ],
    Input({'type': 'scatter_store', 'dataset': ALL, 'index': MATCH}, 'data'),
    [State({'type': 'scatter_dropdown', 'property': ALL, 'index': MATCH}, 'id'),
     State({'type': 'scatter_inputtext', 'property': ALL, 'index': MATCH}, 'id'),

     State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'data'),
     State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'id'),

     ]
)
def fill_scatter_options(sca_options_list,
                         dropdown_state_ids,
                         inputtext_state_ids,
                         table_datasets,  # state, carries the dataframes in record forms
                         table_ids
                         ):
    if len(sca_options_list)!=1:
        print('raise Exception len(sca_options_list)==1 ')
        raise Exception(f'len(sca_options_list) == 1: {sca_options_list}')

    sca_options=sca_options_list[0]

    print(('@@ fill scatter options!'), sca_options, dropdown_state_ids, inputtext_state_ids)
    dataset2records = {tab_id['dataset']: table_datasets[i] for i, tab_id in enumerate(table_ids)}
    fired_dataset, fired_index, fired_type, fired_prop = who_fired()
    out_drop_opt = []
    out_drop_val = []
    out_inputtext = []
    numeric_cols = [k for k, v in dataset2records[fired_dataset][0].items() if type(v) in (int, float)]

    #for sca_options in sca_options_list:
    for dropdown_state_id in dropdown_state_ids:
        if dropdown_state_id['property']=='dataset':
            out_drop_opt.append([ dict(label='Lifehistories', value='Lifehistories'),
                                  dict(label='other...', value='other...')])
            out_drop_val.append('Lifehistories')

        else:
            current_value = sca_options[dropdown_state_id['property']] if sca_options else numeric_cols[0]
            out_drop_opt.append( [ dict(label=colname, value=colname)  for colname in numeric_cols] )
            out_drop_val.append(current_value)

    for inputtext_state_id in inputtext_state_ids:
        current_value = sca_options[inputtext_state_id['property']] if sca_options else ''
        out_inputtext.append(current_value)

    print( '&&&', (out_drop_opt, out_drop_val, out_inputtext) )

    return out_drop_opt, out_drop_val, out_inputtext

########################################################################################################################

@app.callback(
    Output({'type': 'datatable_table', 'dataset': MATCH, 'index': MATCH}, "style_data_conditional"),
    Input({'type': 'datatable_table', 'dataset': MATCH, 'index': MATCH}, "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": tab_color, }
        for i in selRows
    ]


#######################################################################################################################
@app.callback(
    Output({'type': 'scatter_menu',  'index': MATCH}, 'is_open'),
#     Output({'type': 'scatter_menucontainer', 'dataset': MATCH, 'index': MATCH}, 'children'),
     Input({'type': 'scatter_configure', 'index': MATCH}, 'n_clicks'),
     [State({'type': 'scatter_menu',  'index': MATCH}, 'is_open')],
#     [State({'type': 'scatter_store', 'dataset': MATCH, 'index': MATCH}, 'id'),
#      State({'type': 'scatter_store', 'dataset': MATCH, 'index': MATCH}, 'data'),
#      State({'type': 'datatable_table', 'dataset': MATCH, 'index': ALL}, 'data'),
#      State({'type': 'datatable_table', 'dataset': ALL, 'index': ALL}, 'id'),
#      #State('dataframe_store', 'data'),
#      ]
)
def toggle_offcanvas(n_clicks, offcanvas_is_open):
     if n_clicks and not offcanvas_is_open:
         return True
#     dataset2records = {tab_id['dataset']: table_datasets[i] for i, tab_id in enumerate(table_ids)}
#     print('toggle_offcanvas')
#     print(sca_options)
#
#     if n_clicks:
#         return make_scatter_menu(sca_options_id['index'],
#                                  colnames=list(dataset2records[sca_options_id['dataset']][0]), #colnames
#                                  current_options=sca_options
#                                  )
#
#     return None  # is_open

#
# @app.callback(
#     Output({'type': 'scatter_store', 'index': ALL}, 'clear_data'),
#     Input('clear_data_button', 'n_clicks')
# )
# def clear_data_button_clicked(n_clicks):
#     if n_clicks:
#         return [True]
#     else:
#         return [False]


# future:
# callback with pattern matching input: any tree-linked plot -> selected_data___  # fetch the one that fired
# output: set a dcc.store
# another callback input dcc.store, output: pattern matching all tree-linked plot containers; build all plots
## start with three plots (static)
# then move to build plots on demand


if __name__ == '__main__':
    #app.run_server(debug=True)
    run_simple('localhost', 5001, application, use_reloader=True, use_debugger=True, use_evalex=True)
