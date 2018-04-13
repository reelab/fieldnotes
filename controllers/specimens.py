from gluon.serializers import json #for js compatibility of coordinates list

def searchform(fields, url):
    family = Field("family",
            "string",
            required=False,
            widget=SQLFORM.widgets.autocomplete(request,
                db.specimen.family,
                distinct=True,
                limitby=(0,10),
                min_length=1))
    genus = Field("genus",
                "string",
                required=False,
                widget=SQLFORM.widgets.autocomplete(request,
                    db.specimen.genus,
                    distinct=True,
                    limitby=(0,10),
                    min_length=1))
    species = Field("species_epithet",
                "string",
                required=False,
                widget=SQLFORM.widgets.autocomplete(request,
                    db.specimen.species_epithet,
                    distinct=True,
                    limitby=(0,10),
                    min_length=1))
    collector_number = Field("collector_number",
                        "string",
                        required=False,
                        widget=SQLFORM.widgets.autocomplete(request,
                            db.specimen.collector_number,
                            distinct=True,
                            limitby=(0,10),
                            min_length=1))
    form = SQLFORM.factory( family, genus, species, collector_number,
        _method='get',
        _action="#specimen_counter",
        buttons = [TAG.button('Search',_type="submit", _class="btn btn-success mr-4"),
            TAG.button('Clear',_type="reset", _class="btn btn-default btn-primary")])
    return form

def search_function(table, query):
    for k, v in [ (k, v) for k, v in request.vars.items()
                  if (k in table.fields) ]:
        if v:
            query &= (table[k].like("%"+v+"%"))
    return query

def gmap_coordinates(result_set, t):
    coordinates = []
    full_data = db.fullspecimen
    for record in result_set.select(t.specimen_id):
        if record:
            rec = full_data(record.id)
            if rec: #converting minutes/seconds to decimal values
                lat_min = rec['latitude_minutes'] / 60
                lat_sec = rec['latitude_seconds'] / 3600
                lng_min = rec['longitude_minutes'] / 60
                lng_sec = rec['longitude_seconds'] / 3600
                lat_spec = rec['latitude_degrees'] + lat_min + lat_sec
                lng_spec = rec['longitude_degrees'] + lng_min + lng_sec
                coordinates.append({'lat': lat_spec, 'lng': lng_spec})
    return coordinates

def save_to_cabinet(ids):
    return

def index():
    return dict()

def view():
    t = db.fullspecimen
    rec = t(request.args(0))
    rec["place"] = ": ".join(
        [ x for x in (rec["country"], rec["state"], rec["county"], rec["city"]) if x ])
    images_set = db((db.zimage_assoc.image_id==db.zimage.image_id)&(db.zimage_assoc.obj_id==db.specimen.id)&(db.zimage_assoc.assoc_type=='S')&(db.specimen.id==rec.id))
    images_info = images_set.select(db.zimage.ALL)
    return dict(rec=rec, images_info=images_info, images_count=images_set.count())

def search():
    t = db.specimen
    q = (t.id>0) # base query - all records
    if request.vars: #update query if criteria provided
        q = search_function(t,q)
    result_set = db(q)

    fields = (t.specimen_id, t.family, t.genus,
              t.species_epithet, t.collector_number)
    headers = dict( [ (str(x), (str(x).split(".")[1]).capitalize().replace("_", " "))
          for x in fields ])
    links = [lambda row: A('View',_href=URL("view", args=[row.id]))]
    grid = SQLFORM.grid(query=result_set,
                        fields=fields,
                        headers=headers,
                        create=False, deletable=False, editable=False,
                        csv=False, details=False,
                        links=links, #createst the 'view' link for each row
                        search_widget=searchform,
                        #use following attribute to save selection to cabinet
                        selectable=[('Save Selection to Cabinet', lambda ids: save_to_cabinet(ids), 'btn btn-default btn-primary')])


    if grid.elements('th'): #adding select all checkbox
        grid.elements('th')[0].append(SPAN('Select all ', INPUT(_type='checkbox',
            _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);")))

    coordinates = []
    grid.element('.web2py_counter')['_id'] = 'specimen_counter'
    if not request.get_vars: #when form is empty (such as at first load) only show form
        grid = grid.element('.web2py_console form')
    else:
        coordinates = gmap_coordinates(result_set, t) #getting coordinates of results

    coordinates = json(coordinates) # for js compatibility

    return dict(grid=grid, coordinates=coordinates)

def cabinet():
    return dict()
