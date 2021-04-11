from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS, cross_origin

from graphql_backend.schema import schema, Article, ArticleAuthor, Comment, Author
from graphql_backend.db_utils import db_session

app = Flask(__name__)
app.debug = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        get_context=lambda: {'session': db_session}
    )
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
