import json

from django.http import HttpResponse
    
from analytics.sites import gadgets

def data(request, hash):
    gadget = gadgets.get_gadget(int(hash))
    return HttpResponse(json.dumps(gadget.get_data()), mimetype="application/json")
