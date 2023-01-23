from .models import Collection


def collections(request):
    return {'collections': Collection.objects.all()}
