from forum.models import Category

def global_processor(request):
    return {"categories": Category.objects.all()}
