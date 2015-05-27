from django.contrib import admin
from models import Student, Kantor, Trida

class studentAdmin(admin.ModelAdmin):
    list_display = ("prijmeni","jmeno", "trida")

admin.site.register(Student, studentAdmin)

class kantorAdmin(admin.ModelAdmin):
    list_display = ("prijmeni","jmeno")

admin.site.register(Kantor, kantorAdmin)


admin.site.register(Trida)




