from .models import StoreSetting

def store_settings(request):
    return {"settings": StoreSetting.objects.first()}