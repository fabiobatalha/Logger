from pyramid.config import Configurator
from pyramid.events import NewRequest
import pymongo


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # Mongodb Connection
    db_uri = settings['mongodb.db_uri']
    conn = pymongo.Connection(db_uri)
    config.registry.settings['db_conn'] = conn

    config.add_subscriber(add_mongo_db, NewRequest)

    config.scan()
    return config.make_wsgi_app()


def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['mongodb.db_name']]
    event.request.db = db
