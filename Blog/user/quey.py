from django.db.models import Q
def filter_by_category(category):
    if category:
        return Q(category=category)
    else:
        return Q()
def filter_by_author(author):
    if author:
        return Q(author=author)
    else:
        return Q()
    
def filter_by_tags(tags):
    if tags:
        return Q(tags__icontains=tags)
    else:
        return Q()
    
def filter_by_date(date):
    if date:
        start = f"{date} 00:00:00"
        end = f"{date} 23:59:00"
        return Q(created_at__range=(start,end))
    else:
        return Q()