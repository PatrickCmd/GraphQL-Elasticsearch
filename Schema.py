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


class UpdateIndividual(graphene.Mutation):
    
    class Arguments:
        individual_id = graphene.Int()
        first_name = graphene.String()
        last_name = graphene.String()
    individual = graphene.Field(IndividualObject)

    def mutate(self, info, individual_id, **kwargs):
        query_individuals = IndividualObject.get_query(info)
        individual = query_individuals.filter(
            Individual.id == individual_id).first()
        print(individual)
        
        if kwargs.get("first_name"):
            individual.first_name = kwargs["first_name"]
        if kwargs.get("last_name"):
            individual.last_name = kwargs["last_name"]
        individual.update()

        return UpdateIndividual(individual=individual)


class DeleteIndividual(graphene.Mutation):
    
    class Arguments:
        individual_id = graphene.Int(required=True)
    individual = graphene.Field(IndividualObject)

    def mutate(self, info, individual_id):
        query_individuals = IndividualObject.get_query(info)
        individual = query_individuals.filter(
            Individual.id == individual_id).first()
        individual.delete()

        return DeleteIndividual(individual=individual)


class Mutation(graphene.ObjectType):
    create_individual = CreateIndividual.Field()
    update_individual = UpdateIndividual.Field()
    delete_individual = DeleteIndividual.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    individuals = SQLAlchemyConnectionField(IndividualObject)
    individual = graphene.Field(lambda: IndividualObject, id=graphene.Int())
    search_guys = graphene.List(lambda: IndividualObject, search=graphene.String())

    def resolve_individual(self, info, id):
        query = IndividualObject.get_query(info)
        individual = query.filter(Individual.id == id).first()
        
        return individual

    def resolve_search_guys(self, info, search):
        # query = IndividualObject.get_query(info)
        # result = query.filter(or_(Individual.first_name.like('%'+search+'%'),
        #     Individual.last_name.like('%'+search+'%'))).all()
        result = Individual.search(search)
        return result
        
schema = graphene.Schema(query=Query, mutation=Mutation)