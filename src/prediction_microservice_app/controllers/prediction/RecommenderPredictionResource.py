import json

from infrastructor.exception.HybridRecommenderServiceException import HybridRecommenderServiceException
from model.controller.recommender.PredictionRequestModel import PredictionRequestModel
from injector import inject
from controllers.prediction.models.PredictionModels import PredictionModels
from model.controller.CommonModels import CommonModels
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.logging.SqlLogger import SqlLogger
from service.HybridRecommenderService import HybridRecommenderService


@PredictionModels.ns.route("/prediction")
class RecommenderResource(ResourceBase):
    @inject
    def __init__(self,
                 hybridRecommenderService: HybridRecommenderService,
                 log: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hybridRecommenderService = hybridRecommenderService
        self.log = log

    @PredictionModels.ns.expect(PredictionModels.prediction_request_model, validate=True)
    @PredictionModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        This method is endpoint of recommender prediction service.
        """
        self.log.info("Recommender controller is started.")
        try:
            data: PredictionRequestModel = json.loads(json.dumps(IocManager.api.payload),
                                                      object_hook=lambda d: PredictionRequestModel(**d))
            self.log.info("Products: {}".format(data.products))

            result: list = self.hybridRecommenderService.predict(data.products)

            common_result = CommonModels.get_response(result=result, message="recommender succesfully finished.")

            self.log.info("Recommender result: {}".format(result))

        except HybridRecommenderServiceException as ex:
            msg = "Recommender service get an error. Please contact the stuff."
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)
        except Exception as ex:
            msg = "Undefined error is occured. Please contact the stuff. "
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)

        self.log.info("Recommender controller is finished.")

        return common_result
