import re
import urllib.request

import requests


class GaiaDatafilesGetter:

    @staticmethod
    def get_url_root():
        return r'http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv'

    @staticmethod
    def get_files_list():
        content = urllib.request.urlopen(GaiaDatafilesGetter.get_url_root()).read()

        res = re.findall(r'<a href="(GaiaSource[^"]*)"', str(content))

        print("Count of files ", len(res))

        return res

    @staticmethod
    def get_file_request(file):
        url = GaiaDatafilesGetter.get_url_root() + "/" + file
        return requests.get(url)
