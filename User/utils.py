from django.core.serializers.json import DjangoJSONEncoder

from User.models import Profile


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Profile):
            return str(obj)
        return super().default(obj)


