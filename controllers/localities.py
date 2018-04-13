def searchform(fields, url):
    upper_elevation = Field("upper_elevation",
            "integer",
            required=False)
    lower_elevation = Field("lower_elevation",
            "integer",
            required=False)
    country = Field("country",
                "string",
                required=False,
                widget=SQLFORM.widgets.autocomplete(request,
                    db.locality.country,
                    distinct=True,
                    limitby=(0,10),
                    min_length=1))
    state = Field("state",
                "string",
                required=False,
                widget=SQLFORM.widgets.autocomplete(request,
                    db.locality.state,
                    distinct=True,
                    limitby=(0,10),
                    min_length=1))
    county = Field("county",
                "string",
                required=False,
                widget=SQLFORM.widgets.autocomplete(request,
                    db.locality.county,
                    distinct=True,
                    limitby=(0,10),
                    min_length=1))
    city = Field("city",
                "string",
                required=False,
                widget=SQLFORM.widgets.autocomplete(request,
                    db.locality.city,
                    distinct=True,
                    limitby=(0,10),
                    min_length=1))
    form = SQLFORM.factory(country, state, county, city, upper_elevation, lower_elevation,
            _method='get',
            _action="#locality_counter",
            buttons = [TAG.button('Search',_type="submit", _class="btn btn-success mr-4"),
            TAG.button('Clear',_type="reset", _class="btn btn-default btn-primary")])
    return form

def search_function(table, query):
    for k, v in [ (k, v) for k, v in request.vars.items()
                  if (k in table.fields) ]:
        if v:
            query &= (table[k].like("%"+v+"%"))
    return query

def view():
    t = db.locality
    rec = t(request.args(0))
    rec["place"] = ": ".join(
        [ x for x in (rec["country"], rec["state"], rec["county"], rec["city"]) if x ])
    ##images_set = db((db.zimage_assoc.image_id==db.zimage.image_id)&(db.zimage_assoc.obj_id==db.locality.id)&(db.zimage_assoc.assoc_type=='L')&(db.locality.id==rec.id))
    ##images_info = images_set.select(db.zimage.ALL)
    return dict()#rec=rec), images_info=images_info, images_count=images_set.count())

def index():
    t = db.locality
    q = (t.locality_id>0) # base query - all records
    if request.vars: #update query if criteria provided
        q = search_function(t,q)
    result_set = db(q)

    fields = (t.country, t.state, t.county, t.city, t.upper_elevation, t.lower_elevation)
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

    grid.element('.web2py_counter')['_id'] = 'locality_counter'
    if not request.get_vars: #when form is empty (such as at first load) only show form
        grid = grid.element('.web2py_console form')
    return dict(grid=grid)
