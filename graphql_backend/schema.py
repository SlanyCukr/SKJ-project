import datetime
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from database.base_objects import Article as ArticleModel, ArticleAuthor as ArticleAuthorModel, Author as AuthorModel,\
    Comment as CommentModel
from graphql_backend.db_utils import get_comments, get_articles, get_authors_count, get_progress, get_grouped_graph_data,\
    get_categories, get_most_frequent_authors, get_latest_article_time, get_newest_articles


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


class GraphValues(graphene.ObjectType):
    value1 = graphene.Int()
    value2 = graphene.Int()
    date = graphene.Date()


class NumberNamePair(graphene.ObjectType):
    name = graphene.String()
    number = graphene.Int()


class StringDateTimeTuple(graphene.ObjectType):
    value = graphene.String()
    date = graphene.DateTime()


class ArticleInfo(graphene.ObjectType):
    link = graphene.String()
    header = graphene.String()
    category = graphene.String()
    created_on = graphene.DateTime()
    comment_count = graphene.Int()


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
    graph_data = graphene.List(GraphValues)
    categories = graphene.List(NumberNamePair)
    most_frequent_authors = graphene.List(StringDateTimeTuple)
    newest_articles = graphene.List(ArticleInfo)

    def resolve_new_comments(self, info):
        today, day_old, all = get_comments()

        if day_old == 0:
            return CountWithPercent(all, 100)
        percent = (today - day_old) / day_old

        return CountWithPercent(all, percent * 100)

    def resolve_new_articles(self, info):
        today, day_old, all = get_articles()

        if day_old == 0:
            return CountWithPercent(all, 100)
        percent = (today - day_old) / day_old

        return CountWithPercent(all, percent * 100)

    def resolve_current_progress(self, info):
        return get_progress()

    def resolve_authors_count(self, info):
        return get_authors_count()

    def resolve_graph_data(self, info):
        graph_values = []
        comment_counts, article_counts = get_grouped_graph_data()
        for i in range(len(comment_counts)):
            graph_values.append(GraphValues(comment_counts[i][0], article_counts[i][0], datetime.datetime.strptime(article_counts[i][1], "%Y-%m-%d")))
        return graph_values

    def resolve_categories(self, info):
        return [NumberNamePair(x[0], x[1]) for x in get_categories()]

    def resolve_most_frequent_authors(self, info):
        latest_authors = []
        for rec in get_most_frequent_authors():
            latest_authors.append(StringDateTimeTuple(rec[0], datetime.datetime.strptime(get_latest_article_time(rec[1]), "%Y-%m-%d %H:%M:%S.%f")))
        return latest_authors

    def resolve_newest_articles(self, info):
        return [ArticleInfo(x[0], x[1], x[2], datetime.datetime.strptime(x[3], "%Y-%m-%d %H:%M:%S.%f"), x[4]) for x in get_newest_articles()]


schema = graphene.Schema(query=Query)
