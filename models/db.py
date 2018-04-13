# -*- coding: utf-8 -*-
import numbers

host = '107.0.125.182'
db = DAL('mysql://read:only@{}/fieldnotes'.format(host), migrate=False)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] #if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

response.formstyle = 'bootstrap3_stacked' # or 'bootstrap2' or other

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager
## auth = Auth(db)

## create all tables needed by auth if not custom tables
## auth.define_tables(username=False, signature=False)

## ## configure email
## mail = auth.settings.mailer
## mail.settings.server = 'logging' or 'smtp.gmail.com:587'
## mail.settings.sender = 'you@gmail.com'
## mail.settings.login = 'username:password'

## ## configure auth policy
## auth.settings.registration_requires_verification = False
## auth.settings.registration_requires_approval = False
## auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
## from gluon.contrib.login_methods.rpx_account import use_janrain
## use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table(
    "expedition",
    Field("expedition_id", "id"),
    Field("expedition_name", "string"),
    Field("from_date", "datetime"),
    Field("to_date", "datetime"),
    Field("description", "text"),
    migrate=False
    )

db.define_table(
    "locality",
    Field("locality_id", "id"),
    Field("locality_name", "string"),
    Field("latitude_degrees", "integer"),
    Field("latitude_minutes", "integer"),
    Field("latitude_seconds", "integer"),
    Field("north_south", "string"),
    Field("longitude_degrees", "integer"),
    Field("longitude_minutes", "integer"),
    Field("longitude_seconds", "integer"),
    Field("upper_elevation", "integer"),
    Field("lower_elevation", "integer"),
    Field("east_west", "string"),
    Field("country", "string"),
    Field("state", "string"),
    Field("county", "string"),
    Field("city", "string"),
    Field("locality", "text"),
    Field("habitat", "text"),
    migrate=False
    )

db.define_table(
    "localitydd",
    Field("locality_id", "id"),
    Field("locality_name", "string"),
    Field("latitude_degrees", "integer"),
    Field("latitude_minutes", "integer"),
    Field("latitude_seconds", "integer"),
    Field("north_south", "string"),
    Field("longitude_degrees", "integer"),
    Field("longitude_minutes", "integer"),
    Field("longitude_seconds", "integer"),
    Field("lat", "double"),
    Field("lng", "double"),
    Field("upper_elevation", "integer"),
    Field("lower_elevation", "integer"),
    Field("east_west", "string"),
    Field("country", "string"),
    Field("state", "string"),
    Field("county", "string"),
    Field("city", "string"),
    Field("locality", "text"),
    Field("habitat", "text"),
    migrate=False
    )

db.define_table(
    "specimen",
    Field("specimen_id", "id"),
    Field("family", "string", required=False),
    Field("genus", "string", required=False),
    Field("species_epithet", "string", required=False),
    Field("species_author_abbrev", "string", required=False),
    Field("infra_rank", "string", required=False),
    Field("infra_epithet", "string", required=False),
    Field("infra_author_abbrev", "string", required=False),
    Field("determined_by", "string"),
    Field("plant_description", "text", required=False),
    Field("microhabitat", "text"),
    Field("collectors", "text", required=False),
    Field("collector_number", "string", required=False),
    Field("collection_date", "date", required=False),
    Field("number_of_duplicates", "integer", required=False),
    Field("dna_collection", "integer", required=False),
    Field("spirit_dna_comment", "text", required=False),
    Field("sheets_per_duplicate", "integer", required=False),
    Field("expedition_id", db.expedition, required=False, ondelete="NO ACTION"),
    Field("locality_id", db.locality, required=False, ondelete="NO ACTION"),
    Field("group_id", "integer", required=False),
    Field("GLGS_id", "integer", required=False),
    Field("mtime", "datetime", writable=False),
    migrate=False
    )



db.define_table(
    "fullspecimen",
    Field("family", "string", required=False),
    Field("genus", "string", required=False),
    Field("species_epithet", "string", required=False),
    Field("species_author_abbrev", "string", required=False),
    Field("infra_rank", "string", required=False),
    Field("infra_epithet", "string", required=False),
    Field("infra_author_abbrev", "string", required=False),
    Field("determined_by", "string"),
    Field("plant_description", "text", required=False),
    Field("microhabitat", "text"),
    Field("collectors", "text", required=False),
    Field("collector_number", "string", required=False),
    Field("collection_date", "date", required=False),
    Field("number_of_duplicates", "integer", required=False),
    Field("dna_collection", "integer", required=False),
    Field("spirit_dna_comment", "text", required=False),
    Field("sheets_per_duplicate", "integer", required=False),
    Field("expedition_id", db.expedition, required=False, ondelete="NO ACTION"),
    Field("locality_id", db.locality, required=False, ondelete="NO ACTION"),
    Field("group_id", "integer", required=False),
    Field("GLGS_id", "integer", required=False),
    Field("locality_name", "string"),
    Field("latitude_degrees", "integer"),
    Field("latitude_minutes", "integer"),
    Field("latitude_seconds", "integer"),
    Field("north_south", "string"),
    Field("longitude_degrees", "integer"),
    Field("longitude_minutes", "integer"),
    Field("longitude_seconds", "integer"),
    Field("lat", "double"),
    Field("lng", "double"),
    Field("upper_elevation", "integer"),
    Field("lower_elevation", "integer"),
    Field("east_west", "string"),
    Field("country", "string"),
    Field("state", "string"),
    Field("county", "string"),
    Field("city", "string"),
    Field("locality", "text"),
    Field("habitat", "text"),
    migrate=False
    )

db.define_table(
    "zimage",
    Field("image_id", "string"),
    Field("old_imageid", "integer"),
    Field("photographer", "string"),
    Field("image_date", "date"),
    Field("caption", "text"),
    Field("mtime", "datetime"),
    Field("filename", "string"),
    Field("uploaded_by", "string"),
    migrate=False
    )

db.define_table(
    "zimage_assoc",
    Field("assoc_id", "id"),
    Field("image_id", "string", required=True, notnull=True,
          requires=IS_NOT_EMPTY()),
    Field("obj_id", "integer", required=True, notnull=True,
          requires=IS_NOT_EMPTY()),
    Field("assoc_type", "string", required=True, notnull=True,
          requires=IS_IN_SET(['L','S'])),
    migrate=False
    )


HENGDUAN_EXPEDITION_IDS = (
    6, 7, 10, 11, 12, 13, 14, 15, 16, 18, 25, 28, 29, 31, 32, 33, 35, 41, 55, 59, 64)
HENGDUAN_EXPEDITIONS = db.expedition.id.belongs(HENGDUAN_EXPEDITION_IDS)

def fetchspec(q, hengduan=True):
    t = db.specimen
    q &= (t.group_id==1)
    if hengduan:
        q &= t.expedition_id.belongs(HENGDUAN_EXPEDITION_IDS)
    return db(q).select()

def fetchped(x):
    t = db.specimen
    q = (t.genus=='Pedicularis')
    if isinstance(x, basestring):
        p = (t.collector_number==x)
        if db(q & p).count()==0:
            p = (t.species_epithet.like(x))
        return db(q & p).select()
    elif isinstance(x, numbers.Integral):
        q &= (t.collector_number==x)
        if db(q).count():
            return db(q).select()
    else:
        q = (t.genus=='Pedicularis') & x
        return db(q).select()
