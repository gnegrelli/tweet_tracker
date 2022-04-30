from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import UnknownUser
from .services import user_wordcloud


class GetTweetsView(APIView):
    class Meta:
        pass

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            tokens = user_wordcloud(username)
        except UnknownUser:
            return Response({'error': f'Unknown user: {username}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'username': username, 'tokens': tokens}, status=status.HTTP_200_OK)
