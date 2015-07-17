from django.contrib import admin
from models import Student, Teacher, School_class, Ban_reason, User_account_student
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from misc import stringList

class Student_admin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "school_class", "rfid")
    list_display_links = ("surname", )
    search_fields = ("surname", )


class Teacher_admin(admin.ModelAdmin):
    list_display = ("surname", "name")


class School_class_admin(admin.ModelAdmin):
    list_display = ("short_name", "id")


class Ban_reasons_admin(admin.ModelAdmin):
    pass


class User_account_student_resource(resources.ModelResource):

    def get_instance(self, instance_loader, row):
        return False

    def save_instance(self, instance, real_dry_run):
        if not real_dry_run:
            if instance.kod_baka not in stringList(User_account_student.objects.values_list("kod_baka")):
                obj = User_account_student(kod_baka=instance.kod_baka, login=instance.login, email=instance.email)
                obj.save()

    def before_import(self, dataset, dry_run, **kwargs):
        if 'id' not in dataset.headers:
            dataset.headers.append('id')

    class Meta:
        model = User_account_student
        fields = ('kod_baka', 'login', 'email',)

class User_accounts_student_admin(ImportExportActionModelAdmin):
    list_display = ("kod_baka", "login", "default_passwd", "isActive", "banTime", "unbanTime", "autoDeleteTime", "email", "date_generated")
    resource_class = User_account_student_resource







admin.site.register(Student, Student_admin)
admin.site.register(Teacher, Teacher_admin)
admin.site.register(School_class, School_class_admin)
admin.site.register(Ban_reason, Ban_reasons_admin)
admin.site.register(User_account_student, User_accounts_student_admin)





