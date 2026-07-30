from django.db import models

class JobApplication(models.Model):

  STATUS_CHOICES = [
     ('applied', 'Applied'),
     ('interviewing', 'Interviewing'),
     ('rejected', 'Rejected'),
     ('offer', 'Offer'),
  ]
  
  company = models.CharField(max_length=100)
  role = models.CharField(max_length=100)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
  date_applied = models.DateField()
  notes = models.TextField(blank=True)
  job_link = models.URLField(blank=True)

  def __str__(self):
     return f"{self.company} - {self.role}"


class Event(models.Model):
  application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='events')
  date = models.DateField()
  note = models.TextField(blank=True)

  def __str__(self):
    return f"{self.date} - {self.application.company}"
