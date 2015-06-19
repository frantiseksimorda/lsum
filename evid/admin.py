from django.contrib import admin
from models import Student, Teacher, School_class

class studentAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "school_class")
    list_display_links = ('surname', )
    search_fields = ('surname',)


admin.site.register(Student, studentAdmin)

class teacherAdmin(admin.ModelAdmin):
    list_display = ("surname", "name")

admin.site.register(Teacher, teacherAdmin)


class schoolClassAdmin(admin.ModelAdmin):
    list_display = ("short_name", "id" )

admin.site.register(School_class, schoolClassAdmin)




