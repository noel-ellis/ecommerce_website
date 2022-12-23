from .models import Cart, Category


def cart(request):
    return {'cart': Cart.objects.filter(user_id=request.user.id)}


def categories(request):
    return {'categories': Category.objects.all()}
