from snail.view import View


class Homepage(View):

    def get(self, request, *args, **kwargs):
        return 'hello world from view!'