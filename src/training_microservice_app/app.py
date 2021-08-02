import os

from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
from infrastructor.IocManager import IocManager

def start():
    root_directory = os.path.dirname(os.path.abspath(__file__))
    IocManager.configure_startup(root_directory, app_wrapper=FlaskAppWrapper)
    IocManager.run()


if __name__ == "__main__":
    start()
