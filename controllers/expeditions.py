# -*- coding: utf-8 -*-

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

response.title = A(
    'Biodiversity of the Hengduan Mountains | ',
    SPAN('横断山生物多样性', _style='white-space:nowrap'), BR(),
    TAG.small('and adjacent areas of south-central China'),
    _href=URL(), _style="color:white; text-decoration: none !important;"
    )

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    ## response.flash = T('You are successfully running web2py.')
    grid = SQLFORM.grid(db.expedition)
    return dict(grid=grid)
