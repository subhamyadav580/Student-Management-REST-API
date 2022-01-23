from django.contrib import admin
from .models import Course, Subjects


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_ID',
                    'course_name')
    fieldsets = (
        (None, {
            'fields': ('course_ID', 'course_name', 'course_desc')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('course_ID', 'course_name', 'course_desc')}
         ),
    )
    search_fields = ('course_ID',)
    ordering = ('course_name',)
    filter_horizontal = ()

class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('sub_ID',
                    'name')
    fieldsets = (
        (None, {
            'fields': ('sub_ID', 'name', 'course_ID')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('sub_ID', 'name', 'course_ID')}
         ),
    )
    search_fields = ('sub_ID',)
    ordering = ('name',)
    filter_horizontal = ()




admin.site.register(Course, CourseAdmin)
admin.site.register(Subjects, SubjectsAdmin)