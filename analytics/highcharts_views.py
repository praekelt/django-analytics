import json
from random import randint

from django.http import HttpResponse

def data(request, id):
    from analytics.sites import gadgets
    gadget = gadgets.get_gadget(int(id))

    from datetime import datetime
    import time
    #data = [time.mktime(datetime.now().timetuple()) * 1000, Stat.objects.get().value]
    data = [(time.mktime(datetime.now().timetuple()) * 1000, randint(0, 10000)), (time.mktime(datetime.now().timetuple()) * 1000, randint(0, 10000))]
    return HttpResponse(json.dumps(data), mimetype="application/json")
