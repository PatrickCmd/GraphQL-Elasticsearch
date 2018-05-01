from elasticsearch import Elasticsearch
from flask import Flask
from flask_graphql import GraphQLView
from Schema import schema
from sqlalchemy import create_engine
from model import Base,db_session

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

app.add_url_rule('/register',
    view_func=GraphQLView.as_view('register', schema=schema, graphiql=True))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
if __name__ == '__main__':
    app.run(debug=True)