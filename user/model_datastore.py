from flask import current_app
from google.cloud import datastore

builtin_list = list

def init_app(app):
    pass

def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])

def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    print(entity)
    return entity

def list1(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='User')
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor
# [END list]


def read(id):
    ds = get_client()
    key = ds.key('User',int(id))
    results = ds.get(key)
    #print(results)
    return from_datastore(results)

def nemail(uname):

    ds = get_client()
    query = ds.query(kind ='User')
    query.add_filter('email','=',uname)
    
    results = list(query.fetch())
    
    return from_datastore(results)

def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('User', int(id))
    else:
        key = ds.key('User')

    entity = datastore.Entity(
        key=key)
        

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = update

def delete(id):
    ds = get_client()
    key = ds.key('User', int(id))
    ds.delete(key)

