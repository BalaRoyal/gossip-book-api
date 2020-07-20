from rest_framework import generics
from rest_framework import viewsets
from .models import User, UserLocation, Followers
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLocationSerializer, FollowersSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsProfileOwner, IsFollowerOwner
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_email
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site


class BaseUserView(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class BaseFollowView(viewsets.GenericViewSet):
    queryset = Followers.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserListAPIView(BaseUserView,
                      generics.ListCreateAPIView):

    permission_classes = ()
    name = 'list-create-user'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            user_email = validated_data.get('email')
            first_name = validated_data.get('first_name')
            user_id = validated_data.get('id')

            user = serializer.save()
            subject = 'GossipBook Account verification'

            current_site = get_current_site(request)

            html_message = render_to_string('mail_template.html', {
                "name": first_name,
                "activation_token": account_activation_token.make_token(user=user),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'domain': current_site})

            send_email(subject,  html_message, [user_email])

            return Response(
                data={
                    **serializer.data,
                    'message': f"Hi {first_name}!, Thank you for registering with us, Kindly check your email to activate your account."
                },
                status=status.HTTP_201_CREATED)

        except Exception as identifier:
            print(identifier)
            return Response(data={
                "error": f"{identifier}"
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailAPIView(BaseUserView,
                        generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsProfileOwner)
    name = 'user_detail'


class ConfirmEmailAPIVIew(BaseUserView,
                          generics.RetrieveAPIView):
    """
    Activate user account with a valid token sent to their email.
    """

    name = 'activate'
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            import pdb
            pdb.set_trace()
            token = kwargs.get('token')
            uid = int(force_text(urlsafe_base64_decode(kwargs.get('uidb64'))))
            user = get_user_model().objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist) as error:
            import pdb
            pdb.set_trace()

            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(data={
                "message": 'Thank you for your email confirmation. You can now log into your account'
            })

        else:
            return Response(data={"message": "Activation link is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class ListFollowersAPIView(BaseFollowView,
                           generics.ListCreateAPIView):
    """
    List user followers or follow user API Endpoints.
    """

    def get_queryset(self):
        return Followers.objects.filter(user=self.request.user, following=True)

    def perform_create(self, serializer):
        return serializer.save(follower=self.request.user)


class ListFollowingAPIView(BaseFollowView,
                           generics.ListAPIView):
    """
    List user followers or follow user API Endpoints.
    """

    def get_queryset(self):
        return Followers.objects.filter(follower=self.request.user, following=True)


class FollowersDetailView(BaseFollowView, generics.RetrieveUpdateAPIView):
    """
    Retrieve and Update user followers
    """

    permision_classes = (IsAuthenticated, IsFollowerOwner)


class UserInterestedTopicsListAPIView(BaseUserView, generics.ListAPIView):
    """
    List user interested topics.
    """
    pass


class UserInterestedTopicsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    User interested topics API endpoints.
    """

    permission_classes = (IsAuthenticated, IsProfileOwner)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        """
        Adds interested topics to user account.
        """
        topics = None

        if 'interested_topics' in request.data:
            topics = request.data['interested_topics'].split(',')

        if topics:
            user = get_user_model().objects.filter(pk=self.request.user.id).first()

            user.interested_topics.add(**topics)

            user.save()

            return Response(data=self.get_serializer(user).data,
                            status=status.HTTP_200_OK)

        return Response(data={
            'message': 'Data validation error'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Remove interested topics from user account.
    def delete(self, request, *args, **kwargs):
        """
        Remove some topics from user interested topics.
        """
        topics = None

        if 'interested_topics' in request.data:
            topics = request.data['interested_topics'].split(',')
            if topics:
                user = get_user_model().objects.filter(pk=self.request.user.id).first()

                for topic in topics:
                    user.interested_topics.remove(topic)

                return Response(data=self.get_serializer(user),
                                status=status.HTTP_200_OK)
