from graphene import relay
import graphene
from sqlalchemy.sql import or_
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from model import Individual
class IndividualObject(SQLAlchemyObjectType):
    class Meta:
        model = Individual
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    individuals = SQLAlchemyConnectionField(IndividualObject)
    search_guy = graphene.relay.Node.Field(IndividualObject)
    search_guys = graphene.List(lambda:IndividualObject, search=graphene.String())

    def resolve_search_guys(self, info, search):
        query = IndividualObject.get_query(info)
        result = query.filter(or_(Individual.first_name.like('%'+search+'%'),
            Individual.last_name.like('%'+search+'%'))).all()
        return result
        
schema = graphene.Schema(query=Query)