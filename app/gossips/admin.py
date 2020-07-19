from django.contrib import admin
from .models import Gossip, GossipComment

# Register your models here.

admin.site.register(Gossip)
admin.site.register(GossipComment)
