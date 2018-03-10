from django.db import models

class user_details(models.Model):
	rfid = models.CharField(max_length = 50)
	name = models.CharField(max_length = 50)
	age = models.CharField(max_length = 3)
	sex = models.CharField(max_length = 2)
	mobile_no = models.CharField(max_length = 12, default='0000000000')
	appointment_no = models.CharField(max_length = 50, default='Not yet appointed')
	
	def __str__(self):
		return self.rfid + " - " + self.name


class prescription(models.Model):
	# User associated with prescription
	user_associated = models.ForeignKey(user_details, on_delete=models.CASCADE)
	# Doctor associated with user
	doctor_id = models.CharField(max_length=50)
	pres = models.CharField(max_length=500, default='Not yet prescribed')

	symptoms = models.CharField(max_length=100, default="Don't know")
	disease = models.CharField(max_length=100, default='Not yet identified')

	def __str__(self):
		return self.doctor_id + " - " + self.symptoms + " - " + self.disease

		

class doctor(models.Model):
	name = models.CharField(max_length = 50)
	degree = models.CharField(max_length = 100)
	mobile_no = models.CharField(max_length = 12, default='0000000000')
	room_no = models.CharField(max_length = 100)
	max_queue_no = models.CharField(max_length = 50)
	cur_queue_no = models.CharField(max_length = 50, default='1')

	def __str__(self):
		return self.name + " - " + self.cur_queue_no


class queue(models.Model):
	doctor_associated = models.ForeignKey(doctor, on_delete=models.CASCADE)
	user_associated = models.CharField(max_length=50, default=0)
	queue_no = models.CharField(max_length=50)

	def __str__(self):
		return self.queue_no
