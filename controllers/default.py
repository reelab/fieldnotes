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

    grid = SQLFORM.smartgrid(db.locality)

    return dict(grid=grid)

def autocomplete():
    s = request.vars.s or ''
    result = []
    if s:
        w = s.split()
        s = w[0]
        genus = db.specimen.genus
        q = genus.startswith(s)
        rows = db(q).select(
            genus, distinct=True, orderby=genus, limitby=(0,100))
        result = [ x.genus for x in rows ]
        print(result)
    return dict(value=[ dict(value=x) for x in result ])


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


