from django.contrib import admin

from .models import Command, SimpleOutput, TimedMessage

class CommandAdmin(admin.ModelAdmin):
    list_display = ['command', 'get_output', 'permissions']

    def get_fields(self, request, obj=None):
        if None == obj or not obj.is_built_in:
            return ('command', 'permissions', 'output')
        elif obj.is_built_in:
            return ('command', 'permissions')

    def get_output(self, obj):
        return obj.output.output_text if None != obj.output else ''
    get_output.admin_order_field = 'output'
    get_output.short_description = 'Output Text'

    def has_delete_permission(self, request, obj=None):
        if obj:
            return not obj.is_built_in
        else:
            return True

class TimedMessageAdmin(admin.ModelAdmin):
    fields = ['message', 'minutes_interval']
    list_display = ['get_message', 'minutes_interval']

    def get_message(self, obj):
        return obj.message.output_text
    get_message.admin_order_field = 'message'
    get_message.short_description = 'Message'

class SimpleOutputAdmin(admin.ModelAdmin):
    list_display = ['output_text']

admin.site.register(Command, CommandAdmin)
admin.site.register(TimedMessage, TimedMessageAdmin)
admin.site.register(SimpleOutput, SimpleOutputAdmin)
