import os.path
import pickle


HTML_ENV_VAR_PICKLE_FILE_NAME = 'html_env_vars.pickle'
API_BDD_RESPONSE_FILE_NAME = 'api_bdd_response.pickle'


class BPStorage:
    @staticmethod
    def is_api_testing():
        with open('api_testing.pickle', 'rb') as handle:
            return pickle.load(handle)

    @staticmethod
    def set_api_testing(x):
        with open('api_testing.pickle', 'wb') as handle:
            pickle.dump(x, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_env_vars_for_html():
        if os.path.exists(HTML_ENV_VAR_PICKLE_FILE_NAME):
            with open(HTML_ENV_VAR_PICKLE_FILE_NAME, 'rb') as handle:
                return pickle.load(handle)
        else:
            return None

    @staticmethod
    def save_env_vars_for_html(x):
        with open(HTML_ENV_VAR_PICKLE_FILE_NAME, 'wb') as handle:
            pickle.dump(x, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def store_api_bdd_response(response):
        with open(API_BDD_RESPONSE_FILE_NAME, 'wb') as handle:
            pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_api_bdd_response():
        if os.path.exists('api_bdd_response.pickle'):
            with open(API_BDD_RESPONSE_FILE_NAME, 'rb') as handle:
                return pickle.load(handle)
        else:
            return None

