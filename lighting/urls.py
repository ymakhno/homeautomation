from django.conf.urls import patterns, url

from lighting import views

urlpatterns = patterns('',
        url(r'^$', views.main, name="main"),
        url(r'^index$', views.index, name="index"),
        url(r'^cameras$', views.cameras, name="cameras"),
        url(r'^lights$', views.lights, name="lights"),
        url(r'^rules/delete$', views.delete_rule, name="delete.rule"),
        url(r'^rules/add$', views.add_rule, name="add.rule")
)

