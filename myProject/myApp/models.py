from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    
    USER=[
        ('recruiter','Recruiter'),
        ('seeker','Seeker'),
    ]
    user_type=models.CharField(choices=USER,max_length=100,null=True)
    Profile_Pic=models.ImageField(upload_to='Media/Profile_Pic',null=True)
    display_name=models.CharField(max_length=100,null=True)
    
    def __str__(self):   
        
        return f"{self.username}"
    
class seekerProfileModel(models.Model):
    user=models.OneToOneField(customUser,on_delete=models.CASCADE,related_name='seekerProfile')

    SKILLS=[
        ('programming','Programming'),
        ('networking','Networking'),
        ('graphics_design','Graphics Design'),
        ('cyber_security','Cyber Security'),
    ]
    
    skills=models.CharField(choices=SKILLS,max_length=100,null=True)
    
    
   
    def __str__(self):
        return f"{self.user.username}"
    
    
class recruiterProfileModel(models.Model):
    
   
    user = models.OneToOneField(customUser, on_delete=models.CASCADE,related_name='recruiterProfile')
    Company_name=models.CharField(max_length=100,null=True)
   
    def __str__(self):
        return f"{self.user.username}"
    
class JobModel(models.Model):
    JOB_TYPE_CHOICES=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]
    
    SKILLS=[
        ('programming','Programming'),
        ('networking','Networking'),
        ('graphics_design','Graphics Design'),
        ('cyber_security','Cyber Security'),
    ]
    
    
    user=models.ForeignKey(customUser,null=True,blank=True,on_delete=models.CASCADE)

    job_title = models.CharField(max_length=200, null=True, blank=True)  
    number_of_openings = models.PositiveIntegerField( null=True, blank=True) 
    skills=models.CharField(choices=SKILLS,max_length=100,null=True)
    category = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, null=True, blank=True) 
    description = models.TextField(null=True, blank=True)  
    job_Pic=models.ImageField(upload_to='Media/job_Pic',null=True)

    def __str__(self):
        return f"{self.job_title} at {self.category}"
    

class jobApplyModel(models.Model):
    
    user=models.ForeignKey(customUser,on_delete=models.CASCADE,null=True)
    job=models.ForeignKey(JobModel,on_delete=models.CASCADE,null=True)
    Resume = models.FileField(upload_to="Media/Resume",max_length=200, null=True, blank=True) 
    Cover = models.TextField(null=True, blank=True)  
    Skills = models.CharField(max_length=200, null=True, blank=True) 
    image=models.ImageField(upload_to='Media/image',null=True)
    
    
    def __str__(self) -> str:
        return self.user.username+"-"+self.job.job_title
    
  