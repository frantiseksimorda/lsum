from django.contrib import admin
from models import Student, Teacher, School_class

class studentAdmin(admin.ModelAdmin):
    list_display = ("surname", "name", "school_class")

admin.site.register(Student, studentAdmin)

class kantorAdmin(admin.ModelAdmin):
    list_display = ("surname", "name")

admin.site.register(Teacher, kantorAdmin)


admin.site.register(School_class)




