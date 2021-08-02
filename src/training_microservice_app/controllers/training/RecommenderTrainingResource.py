import json

from injector import inject

from controllers.training.models.TrainingModel import TrainingModel
from infrastructor.exception.CartBasedRecommenderServiceException import CartBasedRecommenderServiceException
from infrastructor.exception.ContentBasedRecommenderServiceException import ContentBasedRecommenderServiceException
from infrastructor.exception.EventDataServiceException import EventDataServiceException
from infrastructor.exception.MetaDataServiceException import MetaDataServiceException
from infrastructor.exception.PassedDayBasedRecommenderServiceException import PassedDayBasedRecommenderServiceException
from model.controller.CommonModels import CommonModels
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.logging.SqlLogger import SqlLogger
from service.CartBasedRecommenderService import CartBasedRecommenderService
from service.ContentBasedRecommenderService import ContentBasedRecommenderService
from service.EventDataService import EventDataService
from service.MetaDataService import MetaDataService
from service.PasssedDayBasedRecommenderService import PassedDayBasedRecommenderService


@TrainingModel.ns.route("/training")
class RecommenderResource(ResourceBase):
    @inject
    def __init__(self,
                 metaDataService: MetaDataService,
                 eventDataService: EventDataService,
                 cartBasedRecommenderService: CartBasedRecommenderService,
                 passedDayBasedRecommenderService: PassedDayBasedRecommenderService,
                 contentBasedRecommenderService: ContentBasedRecommenderService,
                 log: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metaDataService = metaDataService
        self.eventDataService = eventDataService
        self.cartBasedRecommenderService = cartBasedRecommenderService
        self.passedDayBasedRecommenderService = passedDayBasedRecommenderService
        self.contentBasedRecommenderService = contentBasedRecommenderService

        self.log = log

    @TrainingModel.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        This method is endpoint of recommender training service.
        """
        self.log.info("Recommender training is started.")
        try:

            self.metaDataService.save_data()
            self.eventDataService.save_data()
            self.cartBasedRecommenderService.fit()
            self.passedDayBasedRecommenderService.fit()
            self.contentBasedRecommenderService.fit()

            common_result = CommonModels.get_response(result="Success", message="Training succesfully is ended")

            self.log.info("Recommender training is finished. You can use API :)")

        except MetaDataServiceException as ex:
            msg = "Meta Data load service service get an error. Please contact the stuff."
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)
        except EventDataServiceException as ex:
            msg = "Event Data load service service get an error. Please contact the stuff."
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)

        except PassedDayBasedRecommenderServiceException as ex:
            msg = "Passed day recommender service get an error. Please contact the stuff."
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)

        except CartBasedRecommenderServiceException as ex:
            msg = "Car base recommender service service get an error. Please contact the stuff."
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)

        except ContentBasedRecommenderServiceException as ex:
            msg = "Content base recommender service get an error. Please contact the stuff."
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)

        except Exception as ex:
            msg = "Undefined error is occured. Please contact the stuff. "
            self.log.error(msg + "err:{}".format(ex))
            common_result = CommonModels.get_error_response(msg)

        return common_result
