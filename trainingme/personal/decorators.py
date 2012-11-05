from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import  RequestContext
from django.utils.decorators import wraps

def owner_required(Model = None):
    """
    The Object must have a function: get_owner_id().
    """
    def _decorator(viewfunc):
        def _closure(request, *args, **kwargs):
            user = request.user
            grant = False
            object_id = args[0]
            object = Model.objects.get(pk=object_id)

            if object.get_owner_id() == request.user.id :
                response = viewfunc(request, *args, **kwargs)
            else:
                response = render_to_response("404.html", {'object': object}, context_instance=RequestContext(request))
                response.status_code = 404

            return response
        return wraps(viewfunc)(_closure)
    return _decorator