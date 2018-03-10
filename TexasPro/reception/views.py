from django.http import HttpResponse
# To work with template
from django.shortcuts import render, get_object_or_404
from .models import user_details, doctor, queue
import os
import os.path

def allot_appointment(request):
	all_obj_user = user_details.objects.all()
	all_obj_doctor = doctor.objects.all()
	rfid =''

	file_path = '/home/nitesh_jindal/input.txt'
	if os.path.isfile(file_path):
		file = open(file_path, 'r+')
		rfid = file.read()
		file.close()
		os.remove(file_path)

	context = {
		'all_obj_user' : all_obj_user ,
		'all_obj_doctor' : all_obj_doctor ,
		'rfid':rfid ,
	}
	return render(request, 'reception/recept.html', context)


def process_appoint(request):
	all_obj_user = user_details.objects.all()
	all_obj_doctor = doctor.objects.all()
	context = {
		'all_obj_user' : all_obj_user ,
		'all_obj_doctor' : all_obj_doctor ,
		'error_message' : "Wrong RFID",
	}
	try:
		required_user_object = get_object_or_404(user_details, rfid = request.POST['rfid_in'])
		required_doctor_object = get_object_or_404(doctor, pk = request.POST['doctor_id'])

		# Max_queue_num is initialized and incremented
		required_doctor_object.max_queue_no = (int)(required_doctor_object.max_queue_no)+1
		if (int)(required_doctor_object.max_queue_no) == 1:
			required_doctor_object.cur_queue_no = '1'

		# New queue number generated and user is associated with it
		new_queue = required_doctor_object.queue_set.create(queue_no = required_doctor_object.max_queue_no)
		new_queue.user_associated = required_user_object.rfid

		# New prescription object is generated
		prescription_object =	required_user_object.prescription_set.create(doctor_id = request.POST['doctor_id'])

		prescription_object.symptoms = request.POST['disease_in']
		required_user_object.appointment_no = new_queue.queue_no


		# new_queue, user's object and doctor's object is saved
		new_queue.save()
		prescription_object.save()
		required_user_object.save()
		required_doctor_object.save()
	except (KeyError, user_details.DoesNotExist):
		return render(request, 'reception/recept.html', context)
	return render(request, 'reception/appointment.html', {'user_object' : required_user_object, 
					'doctor_object': required_doctor_object,
					'prescription_object':prescription_object ,
					 })



def show_doctor_details(request, doctor_id):
	required_doctor_object = get_object_or_404(doctor, pk = doctor_id)
	if request.method == "POST":

		queue = get_object_or_404(required_doctor_object.queue_set, queue_no = request.POST['queue_no'])
		required_user_object = get_object_or_404(user_details, rfid = queue.user_associated)


	elif required_doctor_object.queue_set.all().exists():
		if required_doctor_object.cur_queue_no == '0':
			for next_queue in required_doctor_object.queue_set.all():
				break
			required_doctor_object.cur_queue_no = next_queue.queue_no

		queue = get_object_or_404(required_doctor_object.queue_set, queue_no = required_doctor_object.cur_queue_no)
		required_user_object = get_object_or_404(user_details, rfid = queue.user_associated)

	else:
		required_doctor_object.cur_queue_no = '0'
		required_doctor_object.max_queue_no = '0'
		required_doctor_object.save()
		return render(request, 'reception/doctor.html', {
		'required_doctor_object':required_doctor_object,
		'error_message' : "No patient in the queue",
		})

	prescription_object = get_object_or_404(required_user_object.prescription_set, disease = "Not yet identified", doctor_id = required_doctor_object.pk)
	return render(request, 'reception/doctor.html', {
		'required_doctor_object':required_doctor_object,
		'required_user_object' : required_user_object,
		'prescription_object':prescription_object ,
		})
	
def process_doctor_job(request, doctor_id, rfid_id):
	if(request.method == 'POST'):
		required_doctor_object = get_object_or_404(doctor, pk = doctor_id)
		required_user_object = get_object_or_404(user_details, rfid = rfid_id)

		# Queue is deleted since it's work is over
		if required_user_object.appointment_no != 'Done' and required_user_object.appointment_no != 'Not yet appointed' and required_doctor_object.queue_set.all().exists():
			queue_to_be_deleted = get_object_or_404(required_doctor_object.queue_set, queue_no = required_user_object.appointment_no)
			queue_to_be_deleted.delete()

		# If no queue left, make cur and max_queue_no = 0
		if not required_doctor_object.queue_set.all().exists():
			required_doctor_object.cur_queue_no = '0'
			required_doctor_object.max_queue_no = '0'

		else:
		# Otherwise get the next queue number
			for next_queue in required_doctor_object.queue_set.all():
				break
			required_doctor_object.cur_queue_no = next_queue.queue_no

		if required_user_object.appointment_no != 'Done':
		# Get the prescription object
			required_presciption_object = get_object_or_404(required_user_object.prescription_set, pres= 'Not yet prescribed', doctor_id = required_doctor_object.pk)
			required_presciption_object.pres = request.POST['prescription']
			required_presciption_object.disease = request.POST['disease_in']
			required_presciption_object.save()
			required_user_object.appointment_no = 'Done'
		

		required_doctor_object.save()
		required_user_object.save()

		if required_doctor_object.queue_set.all().exists():
			required_user_object = get_object_or_404(user_details, rfid = next_queue.user_associated)
			return render(request, 'reception/doctor.html', {
				'required_doctor_object':required_doctor_object,
				'required_user_object' : required_user_object,
				})
		else:
			required_doctor_object.cur_queue_no = '0'
			required_doctor_object.max_queue_no = '0'
			return render(request, 'reception/doctor.html', {
			'required_doctor_object':required_doctor_object,
			'error_message' : "No patient in the queue",
			})

	else:
		return show_doctor_details(request, doctor_id)
		

def show_user_details(request, rfid_id):
	required_user_object = get_object_or_404(user_details, rfid = rfid_id)
	all_doctor_object = doctor.objects.all()
	return render(request, 'reception/show_user_details.html', { 'required_user_object':required_user_object ,
																'all_doctor_object':all_doctor_object,
																})