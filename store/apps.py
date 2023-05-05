from django.apps import AppConfig
from watson import search as watson

class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "store"

    def ready(self):
        ProductModel = self.get_model("Product")
        watson.register(ProductModel)
