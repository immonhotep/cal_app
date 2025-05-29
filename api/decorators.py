#custom decorator for fuction based api views, to show browsable api html forms
def serializer(serializer):
    def decorator(api_view):
        api_view.cls.serializer_class = serializer
        api_view.view_class.serializer_class = serializer
        return api_view
    return decorator