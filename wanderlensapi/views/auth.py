from wanderlensapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the wanderlensapi_user table
    user = User.objects.create(
        name=request.data['name'],
        bio=request.data['bio'],
        uid=request.data['uid']
    )

    # Return the user info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'bio': user.bio
    }
    return Response(data)
