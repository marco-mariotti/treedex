# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class EteComponent(Component):
    """An EteComponent component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- activeClades (list of dicts; optional):
    Active clade selections (nodes not saved with name).

- activeLeaves (list of dicts; optional):
    Active leaf selections (nodes not saved with name).

- activeNodes (list of dicts; optional):
    Active node selections (nodes not saved with name).

- height (string; default "100%"):
    iframe height. Default: 100%.

- hover (dict; optional):
    Hovered node.

- path (string; default ""):
    URL from where ETE's server is running.

- saved (dict; optional):
    Saved selections.

    `saved` is a dict with strings as keys and values of type dict
    with keys:

    - color (string; optional)

    - name (string; optional)

    - selectCommand (string; optional)

- treeid (number; required):
    Integer that defines a tree.

- url (string; required):
    URL from where ETE's server is running.

- width (string; default "100%"):
    iframe width. Default: 100%."""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, url=Component.REQUIRED, path=Component.UNDEFINED, treeid=Component.REQUIRED, width=Component.UNDEFINED, height=Component.UNDEFINED, hover=Component.UNDEFINED, activeNodes=Component.UNDEFINED, activeClades=Component.UNDEFINED, activeLeaves=Component.UNDEFINED, saved=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'activeClades', 'activeLeaves', 'activeNodes', 'height', 'hover', 'path', 'saved', 'treeid', 'url', 'width']
        self._type = 'EteComponent'
        self._namespace = 'ete_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'activeClades', 'activeLeaves', 'activeNodes', 'height', 'hover', 'path', 'saved', 'treeid', 'url', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'url', 'treeid']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(EteComponent, self).__init__(**args)
