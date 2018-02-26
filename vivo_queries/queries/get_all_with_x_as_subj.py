from vivo_queries.vdos.thing import Thing

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.vivo_url + params['Thing'].n_number

    return params

def get_query(**params):
    query = """ SELECT ?s ?p ?o WHERE{{<{}> ?p ?o .}} """.format(params['subj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + '\nGenerating triples\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    #Navigate json
    triple_dump = response.json()
    triples = []
    for listing in triple_dump['results']['bindings']:
        pred = listing['p']['value']
        obj = listing['o']['value']
        if 'http://' not in obj and 'https://' not in obj:
            trip = '<' + params['subj'] + '> <' + pred + '> "' + obj + '"'
        else:
            trip = '<' + params['subj'] + '> <' + pred + '> <' + obj + '>'
        triples.append(trip)

    return triples