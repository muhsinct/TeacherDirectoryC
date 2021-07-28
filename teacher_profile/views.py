from .models import Profiles, SubjectsMaster
from django.http import HttpResponseRedirect
from django.conf import settings
import zipfile
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import os
import pandas as pd
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .forms import ProfileImageUploadForm


class ProfilesView(View):
    template_name = 'teacher_profile/profiles.html'

    def get(self, request, *args, **kwargs):
        lastname = request.GET.get("lastname", "")
        subject = request.GET.get("subject", "")
        all_profiles = Profiles.objects.all()

        if lastname:
            all_profiles = all_profiles.filter(last_name__istartswith=lastname)
        if subject:
            all_profiles = all_profiles.filter(subjects__subject_name__istartswith=subject)

        context = {
            'profiles': all_profiles,
            'lastname': lastname,
            'subject': subject
        }
        return render(request, self.template_name, context)


class ProfileDetailsView(View):
    template_name = 'teacher_profile/profile_details.html'

    def get(self, request, *args, **kwargs):
        profile = Profiles.objects.get(pk=kwargs.get('pid'))
        context = {
            'profile': profile
        }
        return render(request, self.template_name, context)


class ImporterView(View):
    template_name = 'teacher_profile/importer.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = ProfileImageUploadForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ProfileImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            images_zip_file = request.FILES['zip_file']
            csv_file = request.FILES['csv_file']
            teacher_details = pd.read_csv(csv_file, delimiter=',')
            n_rows = len(teacher_details)
            teacher_details = teacher_details.dropna(subset=['First Name', 'Email Address'], how='any')
            removed_rows = n_rows - len(teacher_details)

            with open(settings.IMAGE_ROOT.joinpath('images.zip'), 'wb+') as destination:
                for chunk in images_zip_file.chunks():
                    destination.write(chunk)
            images_zip_file = zipfile.ZipFile(settings.IMAGE_ROOT.joinpath('images.zip'), 'r')
            image_name_list = images_zip_file.namelist()

            duplicate_rows = 0
            for index, teacher in teacher_details.iterrows():
                email_id = teacher['Email Address'].strip()
                if email_id:
                    if Profiles.objects.filter(email__iexact=email_id).exists():
                        duplicate_rows = duplicate_rows + 1
                        continue
                profile = Profiles()
                profile.first_name = teacher['First Name'].strip()
                profile.last_name = teacher['Last Name'].strip()
                profile.email = email_id
                profile.phone_number = teacher['Phone Number'].strip()
                profile.room_number = teacher['Room Number'].strip()
                profile.save()
                subjects = teacher['Subjects taught'].strip().split(',')
                if len(subjects) > 5:
                    subjects = subjects[:5]
                for subject in subjects:
                    subject = subject.strip().lower()
                    if subjects != '':
                        subject, created = SubjectsMaster.objects.get_or_create(subject_name=subject)
                        profile.subjects.add(subject)
                image_name = teacher['Profile picture'].strip()
                if image_name in image_name_list:
                    image = images_zip_file.open(image_name, 'r')
                    img = File(image)
                    profile.image_name.save(image_name, img, save=True)
                    image.close()
            images_zip_file.close()
            os.remove(settings.IMAGE_ROOT.joinpath('images.zip'))
            success_rows = n_rows - removed_rows - duplicate_rows
            if success_rows > 0:
                messages.success(request, str(success_rows) + ' profiles added successfully.')
            if removed_rows > 0:
                messages.success(request, str(removed_rows) + ' profiles details are incomplete.')
            if duplicate_rows > 0:
                messages.success(request, str(duplicate_rows) + ' profiles are existing.')
        return render(request, 'teacher_profile/importer.html', {'form': form})


