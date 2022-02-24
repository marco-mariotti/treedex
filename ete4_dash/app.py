# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask import redirect, url_for

import ete_component
from ete4 import Tree
from ete4.smartview.gui.server import run_smartview
from werkzeug.serving import run_simple # werkzeug development server
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Dash app
dash_app = dash.Dash(__name__)
dash_server = dash_app.server


# ETE app
t = Tree("(((a:1,b:1):1,c:1):1, ((e:1, f:1), g:1):1);") # custom tree

ete_path = "/ete"
ete_url = "http://localhost:5000" + ete_path
ete_app = run_smartview(tree=t, tree_name="treedex", run=False, safe_mode=True)

# we need to add ETE's static to Dash app (only root app serves static files)
@dash_server.route(ete_path)
def index():
    return redirect(url_for("static", filename='gui.html', tree=tree))


# GLOBAL APP
application = DispatcherMiddleware(dash_app.server, { ete_path : ete_app })



df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


dash_app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    ete_component.EteComponent(
        id='ete_iframe',
        url=ete_url,
        path=ete_path,
        treeid=0,
        height="700px",
    ),
])


if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True, use_evalex=True)
