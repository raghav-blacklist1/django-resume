from django.contrib.syndication.views import Feed
from django import urls
from home.models import Profile
from home.views import temp2
 
class LatestReg(Feed):
    title = "Meet various people across the globe."
    link = "/temp2/"
    description = ""
 
    def items(self):
        return Profile.objects.all()
 
    def item_title(self, item):
        return item.fname
 
    def item_description(self, item):
        return item.email
 
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return urls.reverse(temp2, args=[item.pk])