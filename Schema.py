from graphene import relay
import graphene
from sqlalchemy.sql import or_
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from model import Individual
class IndividualObject(SQLAlchemyObjectType):
    class Meta:
        model = Individual
        interfaces = (relay.Node, )


class CreateIndividual(graphene.Mutation):
    
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
    individual = graphene.Field(IndividualObject)

    def mutate(self, info, **kwargs):
        individual = Individual(**kwargs)
        individual.save()

        return CreateIndividual(individual=individual)


class DeleteIndividual(graphene.Mutation):
    
    class Arguments:
        individual_id = graphene.Int(required=True)
    individual = graphene.Field(IndividualObject)

    def mutate(self, info, individual_id):
        query_individuals = IndividualObject.get_query(info)
        print(query_individuals)
        individual = query_individuals.filter(
            Individual.id == individual_id).first()
        individual.delete()

        return DeleteIndividual(individual=individual)


class Mutation(graphene.ObjectType):
    create_individual = CreateIndividual.Field()
    delete_individual = DeleteIndividual.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    individuals = SQLAlchemyConnectionField(IndividualObject)
    search_guy = graphene.relay.Node.Field(IndividualObject)
    search_guys = graphene.List(lambda:IndividualObject, search=graphene.String())

    def resolve_search_guys(self, info, search):
        # query = IndividualObject.get_query(info)
        # result = query.filter(or_(Individual.first_name.like('%'+search+'%'),
        #     Individual.last_name.like('%'+search+'%'))).all()
        result = Individual.search(search)
        return result
        
schema = graphene.Schema(query=Query, mutation=Mutation)