# forms.py
from django import forms
from app.models import Categories, Course, Level, Video, UserCourse, Payment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'featured_image', 'featured_video', 'title', 'author', 'category',
            'level', 'description', 'price', 'discount', 'language',
            'Deadline', 'slug', 'status', 'Certificate'
        ]

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        # Add any customization for form fields here if needed
