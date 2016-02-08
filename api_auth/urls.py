from django.conf.urls import url, include
from rest_framework import routers
#from rest_framework.authtoken.views import obtain_auth_token
from api_auth import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'jobs', views.JobViewSet)
router.register(r'activejobs', views.ActiveJobViewSet, base_name='activejobs')
router.register(r'update', views.UpdateViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'liveupdates', views.UpdateViewSet2, base_name='liveupdates')
router.register(r'jobmodifications', views.JobModificationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^api-token-auth/', views.obtain_auth_token),
]
