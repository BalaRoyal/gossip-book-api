from django.contrib import admin
from .models import (Gossip,
                     GossipComment,
                     GossipVote,
                     GossipCommentVote)

# Register your models here.

admin.site.register(Gossip)
admin.site.register(GossipComment)
admin.site.register(GossipVote)
admin.site.register(GossipCommentVote)
