from django.contrib import admin
from models import Student, Teacher, School_class

class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "school_class")
    list_display_links = ("surname", )
    search_fields = ("surname", )


admin.site.register(Student, StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("surname", "name")

admin.site.register(Teacher, TeacherAdmin)


class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("short_name", "id")

admin.site.register(School_class, SchoolClassAdmin)




