from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image

# Maybe check for another model structure for the different user 
class Profile(models.Model):
    #similaire
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    picture = models.ImageField(default='default.png', upload_to='profile_pics')
    accountLevel = models.IntegerField(default=0) # 0 for student, 1 for helper, ...
    asked_helper = models.BooleanField(default=False) # If user wants to be helper, this is true.
    
    #Student
    classId = models.ForeignKey('HelpArcApp.class', on_delete=models.SET_NULL, blank=True, null=True)

    #Helper
    titleId = models.ForeignKey('HelpArcApp.Title', on_delete=models.SET_NULL, blank=True, null=True)
    #skills = models.ManyToManyField('HelpArcApp.Technology', through='HelpArcApp.SkillLevels')
    is_complete = models.BooleanField(default=False)
     

    # specialized_profile = models.OneToOneField(AbstractSpecializedProfile, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Profile'

