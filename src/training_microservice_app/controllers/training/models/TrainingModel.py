from infrastructor.IocManager import IocManager


class TrainingModel:
    ns = IocManager.api.namespace('recommender', description='recommender endpoints', path='/api/recommender')
