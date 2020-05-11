from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from PIL import Image

User = settings.AUTH_USER_MODEL


class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



class Profile_Query_set(models.QuerySet):
    def search(self, query):
        usersLookup =  Q(user__username__icontains= query) | Q(user__first_name__icontains= query) | Q(user__last_name__icontains= query) | Q(location__icontains= query) | Q(bio__icontains= query)
        return self.filter(usersLookup).distinct()
    def searchUsername(self, query):
        userLookup = Q(user__username= query)
        return self.filter(usersLookup).distinct()

class ProfileManager(models.Manager):

    def get_queryset(self):
        return Profile_Query_set(self.model, using=self._db)

    def search(self,query):
        return self.get_queryset().search(query)
    
    def searchByUsername(self, query):
        return self.get_queryset().searchUsername(query)

# class Interest(models.Model):
#     interest = models.CharField(_("interest"), max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=220, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # interests = models.ManyToManyField, verbose_name=_("") 
    # is_mentee = models.BooleanField(_("Mentee_check"),default=False)
    # is_mentor = models.BooleanField(_("Mentor_check"),default=False)
    
    """
    project_obj = Profile.objects.first()
    project_obj.followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 and img.width > 300:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

        elif img.height > 300:
            output_size = (300, img.width)
            img.thumbnail(output_size)
            img.save(self.image.path)

        elif img.width > 300:
            output_size = (img.height, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    objects = ProfileManager()

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)

# after the user logs in -> verify profile