from infrastructor.IocManager import IocManager

from flask_restplus import fields


class PredictionModels:
    ns = IocManager.api.namespace('recommender', description='recommender endpoints', path='/api/recommender')

    prediction_request_model = IocManager.api.model('PredictionRequestModel', {
        'products': fields.List(fields.String(example="HB001", required=True), min_items=1, unique=True)
    })
