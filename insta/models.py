from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import pyperclip
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


class Category(models.Model):
    """
    This is the class where we will create categories
    """
    name = models.CharField(max_length=30)

    def save_category(self):
        """
        This is the function that we will use to save the instance of this class
        """
        self.save()

    def delete_category(self):
        """
        This is the method to delete the instance
        """
        Category.objects.get(id=self.id).delete()

    def update_category(self, field, val):
        """
        This is the method to update the instance
        """
        Category.objects.get(id=self.id).update(field=val)

    def __str__(self):
        return self.name


class Image(models.Model):
    image= models.ImageField(upload_to="images/")
    name = models.CharField(max_length=30)
    caption = models.TextField()
    location = models.ForeignKey(Location)
    category = models.ForeignKey(Category)
    pub_date = models.DateTimeField(auto_now_add=True)

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
    def show_image(cls, category):
        images = cls.objects.filter(category_name=category)
        return images

    @classmethod
    def get_photos(cls):
        return cls.objects.all()

    @classmethod
    def search_by_category(cls, category):
        photo = Category.objects.filter(name_icontains=category)[0]
        return cls.objects.filter(category_id=photo.id)

    @classmethod
    def filter_by_location(cls, location):
        """
        The method to get images taken in a certain location
        """
        the_location = Location.objects.get(name=location)
        return cls.objects.filter(location_id=the_location.id)

    def __str__(self):
        return self.name
