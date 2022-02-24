import dash, re

prop_id_pattern=      re.compile('\{"dataset":"(.+)","index":(\d+),"type":"(.+)"\}\.(.+)$')
prop_id_pattern_no_ds=re.compile('\{"index":(\d+),"type":"(.+)"\}\.(.+)$')

def who_fired(no_ds=False):
    #id_fired, prop_fired = .split('.')
    #print(f'pre who_fired: {dash.callback_context.triggered}')
    x=dash.callback_context.triggered[0]['prop_id']
    print(f'who_fired: {x}')
    if x!='.':
        if no_ds:
            strindex, fired_type, fired_prop = prop_id_pattern_no_ds.search(x).groups()
        else:
            fired_dataset, strindex, fired_type, fired_prop = prop_id_pattern.search(x).groups()
        fired_index=int(strindex)

    else:
        if no_ds:
            fired_index, fired_type, fired_prop = (None, None, None)
        else:
            fired_dataset, fired_index, fired_type, fired_prop = (None, None, None, None)

    if no_ds:
        return fired_index, fired_type, fired_prop
    else:
        return fired_dataset, fired_index, fired_type, fired_prop
