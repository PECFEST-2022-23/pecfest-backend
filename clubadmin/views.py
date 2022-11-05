from functools import partial

from events.models import Event
from events.serializers import EventSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

# Create your views here.


class EventAPIView(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def post(self, request):
        data = request.data
        club = request.user.club
        data["club"] = club.id  # add club id to the data
        serializer = self.get_serializer(data=data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()  # save event

        response_data = {"message": "Event created"}
        response_data["event_id"] = serializer.data["id"]
        return Response(response_data, status.HTTP_201_CREATED)

    def delete(self, request, event_id, *args, **kwargs):
        try:
            event = self.get_queryset().get(id=event_id)
        except:
            return Response(
                {"error": "event does not exists"}, status.HTTP_404_NOT_FOUND
            )  # return error if event doesn't exists

        event.delete()
        response_data = {"message": "event deleted"}
        return Response(response_data, status.HTTP_200_OK)

    def patch(self, request, event_id, *args, **kwargs):
        data = request.data
        club = request.user.club
        data["club"] = club.id  # add club id to the data

        try:
            event = self.get_queryset().get(
                id=event_id
            )  # fetch the event to be modified
        except:
            return Response(
                {"error": "event does not exists"}, status.HTTP_404_NOT_FOUND
            )  # return error if event doesn't exists

        # verify if the user and event belong to the same club
        if str(event.club_id) != str(club.id):
            return Response({"error": "access denied"}, status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(
            event, data=data, context={"user": request.user}, partial=True
        )  # create serializer
        serializer.is_valid(raise_exception=True)
        serializer.save()  # update

        response_data = {"message": "Event modified"}
        response_data["event_id"] = event_id
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        club_id = request.user.club_id
        try:
            event_objs = Event.objects.filter(club_id=club_id)
        except Exception:
            return Response(
                {"message": "Invalid club id"}, status=status.HTTP_400_BAD_REQUEST
            )
        if event_objs:
            serializer = EventSerializer(event_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Invalid club id"}, status=status.HTTP_400_BAD_REQUEST
            )
