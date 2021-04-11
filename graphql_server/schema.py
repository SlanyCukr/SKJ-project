import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.base_objects import Article as ArticleModel, ArticleAuthor as ArticleAuthorModel, Author as AuthorModel,\
    Comment as CommentModel


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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_articles = SQLAlchemyConnectionField(Article.connection)
    # Disable sorting over this field
    all_authors = SQLAlchemyConnectionField(Author.connection, sort=None)


schema = graphene.Schema(query=Query)
