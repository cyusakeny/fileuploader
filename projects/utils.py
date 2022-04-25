from django.core.serializers.json import DjangoJSONEncoder

from projects.models import SharedFile


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, SharedFile):
            return str(obj)
        return super().default(obj)
