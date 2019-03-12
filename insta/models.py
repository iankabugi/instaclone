from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import pyperclip
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Location(models.Model):
    """
    This is the class where we will create locations
    """
    name = models.CharField(max_length=30)

    def save_location(self):
        """
        This is the function that we will use to save the instance of this class
        """
        self.save()

    def delete_location(self):
        """
        This is the method to delete the instance
        """
        self.delete()

    def update_location(self, field, val):
        """
        This is the method to update the instance
        """
        Location.objects.get(id=self.id).update(field=val)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Class that contains profile details
    """
    bio = HTMLField()
    dp = models.ImageField(upload_to='images/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null="True")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    post_save.connect(save_user_profile, sender=User)

    def save_profile(self):
        self.save()

    def del_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        profile = cls.objects.filter(user__username__icontains=name)
        return profile

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(id=id)
        return profile
    @classmethod
    def update_profile(cls, id, profile):
        profile = cls.objects.get(pk=id)
        profile = cls(profile=profile)
        profile.save()



class Image(models.Model):
    imager = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=30)
    caption = models.TextField()
    profile = models.ForeignKey(Profile)
    posted_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def save_image(self):
        """
        The function that we will use to save the instance of this class
        """
        self.save()

    def delete_image(self):
        """
        The function that we will use to delete the instance of this class
        """
        Image.objects.get(id=self.id).delete()

    def update_image(self, val):
        """
        The method to update the instance
        """
        Image.objects.filter(id=self.id).update(name=val)

    @classmethod
    def get_image_by_id(cls, image_id):
        """
        The method to get a specific image
        """
        return cls.objects.get(id=image_id)

    @classmethod
    def copy_image(image):
        find_image = Image.get_image_by_id(image_id)
        return pyperclip.copy(find_image.image)

    @classmethod
    def show_image(cls, profile):
        images = cls.objects.filter(profile_name=profile)
        return images

    @classmethod
    def get_photos(cls):
        return cls.objects.all()

    @classmethod
    def search_by_profile(cls, profile):
        photo = Profile.objects.filter(name_icontains=profile)[0]
        return cls.objects.filter(profile_id=photo.id)

    @classmethod
    def filter_by_location(cls, location):
        """
        The method to get images taken in a certain location
        """
        the_location = Location.objects.get(name=location)
        return cls.objects.filter(location_id=the_location.id)

    def __str__(self):
        return self.name


class Comments(models.Model):
    """
    Class that contains comments details
    """
    comment = HTMLField()
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null="True")
    posted_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['posted_on']

    def save_comm(self):
        self.save()

    def del_comm(self):
        self.delete()

    @classmethod
    def get_comments_by_image_id(cls, image):
        comments = Comments.objects.get(image_id=image)
        return comments


class Preference(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.image) + ':' + str(self.value)

    class Meta:
        unique_together = ("user", "image", "value")
