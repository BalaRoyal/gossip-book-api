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
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from utils.signals import follow_user_signal
from gossips.models import GossipComment, Gossip
from question.models import QuestionComment, Question
from gossips.serializers import GossipCommentSerializer
from question.serializers import QuestionCommentSerializer
import os


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = ()


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    authentication_classes = ()


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

            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(data={
                "message": 'Thank you for your email confirmation. You can now log into your account'
            })

        else:
            return Response(data={"message": "Activation link is invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class ListFollowersAPIView(BaseFollowView,
                           generics.ListCreateAPIView):
    """
    List user followers or follow user API Endpoints.
    """

    def get_queryset(self):
        return Followers.objects.filter(user=self.request.user, following=True)

    def perform_create(self, serializer):
        instance = serializer.save(follower=self.request.user)
        follow_user_signal.send(
            instance=instance, user=self.request.user, created=True)
        return instance


class ListFollowingAPIView(BaseFollowView,
                           generics.ListAPIView):
    """
    List user followers or follow user API Endpoints.
    """

    def get_queryset(self):
        return Followers.objects.filter(follower=self.request.user, following=True)


class ListUserAnswer(generics.ListAPIView):
    """List all comments adde to either user questions/ answers"""

    serializer_class = QuestionCommentSerializer

    def get_queryset(self):
        questions = Question.objects.filter(user=self.request.user)
        comments = QuestionComment.objects.filter(question__in=questions)

        return comments


class ListUserGossipComments(generics.ListAPIView):
    """List all comments adde to either user questions/ answers"""

    serializer_class = GossipCommentSerializer

    def get_queryset(self):
        gossips = Gossip.objects.filter(user=self.request.user)
        answers = GossipComment.objects.filter(gossip__in=gossips)

        return answers


class FollowersDetailView(BaseFollowView, generics.RetrieveUpdateAPIView):
    """
    Retrieve and Update user followers
    """

    permission_classes = (IsAuthenticated, IsFollowerOwner)


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


class InitConfigView(generics.ListAPIView):

    permission_classes = ()
    queryset = get_user_model().objects.all()
    serializer_class = ()

    def get(self, request, *args, **kwargs):

        init_user_email = os.environ.get('INITIAL_EMAIL')
        init_user_username = os.environ.get('INITIAL_USERNAME')
        init_user_password = os.environ.get('INITIAL_PASSWORD')

        try:
            user = get_user_model().objects.filter(email=init_user_email).first()

            if user:
                pass
            else:
                get_user_model().objects.create_superuser(email=init_user_email,
                                                          username=init_user_username, password=init_user_password)
        except Exception as error:
            return Response(data={
                'error': f"Failed to create initial user {error}"
            })

        return Response(data={'message': "Initial admin user was created successfully!"})
