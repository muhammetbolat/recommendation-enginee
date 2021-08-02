from datetime import datetime

from injector import inject

from repository.base.DatabaseSessionManager import DatabaseSessionManager
from repository.base.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.ConsoleLogger import ConsoleLogger
from model.entity.Log import Log


class SqlLogger(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 console_logger: ConsoleLogger):
        super().__init__()
        self.database_session_manager = database_session_manager
        self.console_logger = console_logger

    def log_to_db(self, level, message):

        self.console_logger.info(f'{level} - {message}')

        log_repository: Repository[Log] = Repository[Log](self.database_session_manager)
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        try:
            log = Log(level=level, message=message[0:4000], logDatetime=log_datetime)
            log_repository.insert(log)
            self.database_session_manager.commit()

        except Exception as ex:
            self.console_logger.error(f'Sql logging getting error {ex}')
        finally:
            self.database_session_manager.close()

    def error(self, message):
        self.log_to_db("ERROR", message)

    def info(self, message):
        self.log_to_db("INFO", message)

    def debug(self, message):
        self.log_to_db("DEBUG", message)
