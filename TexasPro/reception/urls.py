from django.conf.urls import url, include
from . import views

app_name = 'reception'

urlpatterns = [

	# For showing 1st - reception page
	# /
	url(r'^$', views.allot_appointment, name='index'),

	# Processing page after appointment that'll redirect to show user's appointment
	# /processing/
	url(r'processing/$', views.process_appoint, name = 'process_appoint'),

	# For showing Doctor's page
	# doctor/<doctor_id>/
	url(r'^doctor/(?P<doctor_id>[0-9]+)/$', views.show_doctor_details, name = 'doctor'),

	# After completion of Doctor's Job
	# doctor/<doctor_id>/<rfid>/done/
	url(r'^doctor/(?P<doctor_id>[0-9]+)/(?P<rfid_id>[0-9]+)/done/$', views.process_doctor_job, name = 'doctor_job_complete'),

	# For showing User's page
	# user/<rfid>/
	url(r'^user/(?P<rfid_id>[0-9]+)/$', views.show_user_details, name = 'user'),

	]