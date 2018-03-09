response.title = SPAN(
    'Biodiversity of the Hengduan Mountains | ',
    SPAN('横断山生物多样性', _style='white-space:nowrap'), BR(),
    TAG.small('Specimens')
    )


def index():
    family = Field("family", "string", required=False)
    genus = Field("genus", "string", required=False)
    species = Field("species_epithet", "string", required=False)
    collector_number = Field("collector_number", "string", required=False)

    ##action = URL('search.load')
    form = SQLFORM.factory(
        family, genus, species, collector_number,
        _id="searchform")
    results = None

    if form.process(keepvalues=True).accepted:
        response.flash = 'form accepted'
        t = db.specimen
        q = (t.id>0)
        if request.vars:
            for k, v in [ (k, v) for k, v in request.vars.items()
                          if (k in t.fields) ]:
                if v:
                    q &= (t[k].like("%"+v+"%"))

        fields = (t.specimen_id, t.family, t.genus,
                  t.species_epithet, t.collector_number)
        rows = db(q).select(*fields)
        headers = dict(
            [ (str(x), (str(x).split(".")[1]).capitalize().replace("_", " "))
              for x in fields ]
            )
        results = SQLTABLE(rows, headers=headers)

        ##response.js =  "$('#results').removeClass('hide_from_view')"
        ##response.js =  'jQuery("#%s").show("slow");' % "results"



    return dict(form=form, results=results)

def view():
    t = db.fullspecimen
    rec = t(request.args(0))
    rec["place"] = ": ".join(
        [ x for x in (rec["state"], rec["county"], rec["city"]) if x ])
    return dict(rec=rec)

def search():
    t = db.specimen
    q = (t.id>0)
    for k, v in [ (k, v) for k, v in request.vars.items()
                  if (k in t.fields) ]:
        if v:
            q &= (t[k].like("%"+v+"%"))
    fields = (t.specimen_id, t.family, t.genus,
              t.species_epithet, t.collector_number)
    rows = db(q).select(*fields)
    headers = dict(
        [ (str(x), (str(x).split(".")[1]).capitalize().replace("_", " "))
          for x in fields ]
        )
    results = SQLTABLE(rows, headers=headers)

    return dict(results=results)

def load_record():
    i = int(request.args(0) or 0)
    return LOAD("specimen", "record.load",
                args=[i], vars=request.vars, ajax=True)

def record():
    t = db.specimen
    rec = t(int(request.args(0) or 0))
    form = SQLFORM(t, rec, _id="recordform", showid=False)
    if form.accepts(request):
        response.flash = "record updated"
    return dict(form=form)

def distinct_species():
    q = db.specimen.id>0
    if request.vars.term:
        q = db.specimen.species.like(request.vars.term+"%")
    rows = db(q).select(db.specimen.species,
                        distinct=True,
                        orderby=db.specimen.species)
    return dict(results=[ dict(id=i, label=r.species, value=r.species)
                          for i, r in enumerate(rows) if r.species ])
