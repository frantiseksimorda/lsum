from evid.models import Email_changes, Error_log

def any_changes(request):
    return {'any_changes': len(Email_changes.objects.all()) > 0}

def error_log_full(request):
    return {'error_log_full': len(Error_log.objects.all()) > 0}