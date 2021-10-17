from snail.urls import Url
from views import Homepage


urlpatterns = [
    Url('^$', Homepage),
]