import datetime
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from database.base_objects import Article as ArticleModel, ArticleAuthor as ArticleAuthorModel, Author as AuthorModel,\
    Comment as CommentModel
from graphql_backend.db_utils import get_comments, get_articles, get_authors_count, get_progress, get_grouped_comments,\
    get_categories


class Article(SQLAlchemyObjectType):
    class Meta:
        model = ArticleModel
        interfaces = (relay.Node, )


class ArticleAuthor(SQLAlchemyObjectType):
    class Meta:
        model = ArticleAuthorModel
        interfaces = (relay.Node, )


class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        interfaces = (relay.Node, )


class Author(SQLAlchemyObjectType):
    class Meta:
        model = AuthorModel
        interfaces = (relay.Node, )


class CountWithPercent(graphene.ObjectType):
    count = graphene.Int()
    percent = graphene.Int()


class GraphValue(graphene.ObjectType):
    value = graphene.Int()
    date = graphene.Date()


class NumberNamePair(graphene.ObjectType):
    name = graphene.String()
    number = graphene.Int()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_articles = SQLAlchemyConnectionField(Article.connection)
    # Disable sorting over this field
    all_authors = SQLAlchemyConnectionField(Author.connection, sort=None)

    new_comments = graphene.Field(CountWithPercent)
    new_articles = graphene.Field(CountWithPercent)
    current_progress = graphene.Int()
    authors_count = graphene.Int()
    latest_comments_graph = graphene.List(GraphValue)
    categories = graphene.List(NumberNamePair)

    def resolve_new_comments(self, info):
        today, day_old, all = get_comments()

        percent = (today - day_old) / day_old

        return CountWithPercent(all, percent * 100)

    def resolve_new_articles(self, info):
        today, day_old, all = get_articles()

        day_old += 1 # only temporarily, until we have enough data
        percent = (today - day_old) / day_old

        return CountWithPercent(all, percent * 100)

    def resolve_current_progress(self, info):
        return get_progress()

    def resolve_authors_count(self, info):
        return get_authors_count()

    def resolve_latest_comments_graph(self, info):
        return [GraphValue(x[0], datetime.datetime.strptime(x[1], "%Y-%m-%d")) for x in get_grouped_comments()]

    def resolve_categories(self, info):
        return [NumberNamePair(x[0], x[1]) for x in get_categories()]


schema = graphene.Schema(query=Query)
