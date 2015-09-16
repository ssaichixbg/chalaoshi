import sae
from main_app import wsgi

debug = False

application = None
if debug:
    from sae.ext.shell import ShellMiddleware
    application = sae.create_wsgi_app(ShellMiddleware(wsgi.application))
else:
    application = sae.create_wsgi_app(wsgi.application)