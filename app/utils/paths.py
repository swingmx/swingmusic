import sys


def getFlaskOpenApiPath():
    """
    Used to retrieve the path to the flask_openapi3 package

    See: https://github.com/luolingchun/flask-openapi3/issues/147
    """
    site_packages_path = [p for p in sys.path if "site-packages" in p][0]

    return f"{site_packages_path}/flask_openapi3"
