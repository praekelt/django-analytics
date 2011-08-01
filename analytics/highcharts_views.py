import json

from django.http import HttpResponse

def data(request, hash):
    from analytics.sites import gadgets
    gadget = gadgets.get_gadget(int(hash))
    return HttpResponse(json.dumps(gadget.get_data()), mimetype="application/json")
