from datetime import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from events.serializers import EventSerializer
from events.validator import EventCreateInputValidator
from users.models import OrganisationCommittee
from users.serializers import UserSerializer

from . import models

from .models import Event
from django.shortcuts import render
from django.db.models import Q

# def search_events(request):
#     results = []
#     if request.method == "POST":
#         query = request.POST.get('name', '')  # Get the search input from form
#         results = Event.objects.filter(name__icontains=query)  # Search for matching events


#     return render(request, 'events/search_results.html', {'results': results})


class EventCreateAPI(APIView):
    """API view to create new events

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to create new events

        Input Serializer:
            - title
            - description
            - start_time
            - end_time
            - location
            - organisation_id

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
                - Organisation not found (organisation_id field)
            - Successes
                - success message
        """

        organisation_id = request.data.get("organisation_id")

        organisation = OrganisationCommittee.objects.filter(
            organisation__id=organisation_id, user=request.user
        ).first()

        if not organisation:
            return Response(
                {"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND
            )

        validated_data = EventCreateInputValidator(request.data).serialized_data()

        event = models.Event(
            name=validated_data.get("name"),
            scan_id=validated_data.get("scan_id"),
            description=request.data.get("description"),
            start_datetime=request.data.get("start_datetime"),
            end_datetime=request.data.get("end_datetime"),
            location=request.data.get("location"),
            latitude=request.data.get("latitude"),
            longitude=request.data.get("longitude"),
            category=request.data.get("category"),
            tags=request.data.get("tags"),
            type=request.data.get("type"),
            status="draft",
            organisation=organisation.organisation,
            created_by=request.user,
        )
        event.save()

        return Response(
            {
                "success": "Event created",
                "details": EventSerializer(event).details_serializer(),
            },
            status=status.HTTP_201_CREATED,
        )


class EventsPublicFeedAPI(APIView):
    """API view to fetch events feed

    Methods:
        GET
    """

    permission_classes = []
    authentication_classes = []

    class CustomPaginator(PageNumberPagination):
        """Custom paginator for this view only"""
        page_size = 25  # Set page size to 25
        # page_size_query_param = 'page_size'  # Optional: Allow users to override page size
        # max_page_size = 100  # Prevent excessive page sizes

    def get(self, request):
        """GET Method to fetch events feed

        Output Serializer:
            - EventsFeedSerializer

        Possible Outputs:
            - Errors
                - None
            - Successes
                - events feed
        """
        search_query = request.GET.get("search", "").strip()
        
        # Fetch all upcoming published events
        events = models.Event.objects.filter(
            status="published", start_datetime__gte=timezone.now()
        ).order_by("start_time")

        # Apply search filtering if user has entered a keyword
        if search_query:
            events = events.filter(
                Q(name__icontains=search_query) |  # Search in event name
                Q(description__icontains=search_query) |  # Search in event description
                Q(location__icontains=search_query)  # Search in event location
            )


        # Retrieve query parameters
        category = request.GET.get("category")
        event_type = request.GET.get("type")
        tags = request.GET.getlist("tags")  # Handles multiple tags
        # Get sorting parameters from the request
        sort_by = request.GET.get("sort_by", "start_datetime")  # Default to start_datetime
        order = request.GET.get("order", "asc")  # Default to ascending order

        # Define allowed sorting fields
        allowed_sort_fields = ["start_datetime", "name", "scan_id"]

        # Ensure sort_by is valid
        if sort_by not in allowed_sort_fields:
            sort_by = "start_datetime"  # Default to start_datetime if invalid

        # Apply sorting order
        if order == "desc":
            sort_by = f"-{sort_by}"  # Prefix '-' for descending order

        # Apply sorting
        events = events.order_by(sort_by)

        events = models.Event.objects.filter(
            status="active", start_time__gte=timezone.now()
        ).order_by("start_time")

        if category:
            events = events.filter(category=category)
        if event_type:
            events = events.filter(type=event_type)
        if tags:  # Assuming tags is a JSONField containing a list
            events = events.filter(tags__contains=tags)


        events = events.order_by("start_datetime")  # Order by date

        # Apply pagination (Only for this view)
        paginator = self.CustomPaginator()
        paginated_events = paginator.paginate_queryset(events, request)

        return paginator.get_paginated_response(
            {
                "events": [
                    {
                        "details": EventSerializer(event).details_serializer
                    }
                    for event in paginated_events
                    
                ]
            },
            status=status.HTTP_200_OK,
        )


class EventsFeedAPI(APIView):
    # ! need to add search, filter and pagination
    """API view to fetch events feed

    Methods:
        GET
    """

    permission_classes = []

    class CustomPaginator(PageNumberPagination):
            """Custom paginator for this view only"""
            page_size = 25  # Set page size to 25
            # page_size_query_param = 'page_size'  # Optional: Allow users to override page size
            # max_page_size = 100  # Prevent excessive page sizes

    def get(self, request):
        """GET Method to fetch events feed

        Output Serializer:
            - EventsFeedSerializer

        Possible Outputs:
            - Errors
                - None
            - Successes
                - events feed
        """
        search_query = request.GET.get("search", "").strip()

        # Fetch all upcoming published events
        events = models.Event.objects.filter(
            status="published", start_datetime__gte=timezone.now()
        ).order_by("start_time")

        # Apply search filtering if user has entered a keyword
        if search_query:
            events = events.filter(
                Q(name__icontains=search_query) |  # Search in event name
                Q(description__icontains=search_query) |  # Search in event description
                Q(location__icontains=search_query)  # Search in event location
            )

        # Retrieve query parameters
        category = request.GET.get("category")
        event_type = request.GET.get("type")
        tags = request.GET.getlist("tags")  # Handles multiple tags
        # Get sorting parameters from the request
        sort_by = request.GET.get("sort_by", "start_datetime")  # Default to start_datetime
        order = request.GET.get("order", "asc")  # Default to ascending order

        # Define allowed sorting fields
        allowed_sort_fields = ["start_datetime", "name", "scan_id"]

        # Ensure sort_by is valid
        if sort_by not in allowed_sort_fields:
            sort_by = "start_datetime"  # Default to start_datetime if invalid

        # Apply sorting order
        if order == "desc":
            sort_by = f"-{sort_by}"  # Prefix '-' for descending order

        # Apply sorting
        events = events.order_by(sort_by)

        events = models.Event.objects.filter(
            status="active", start_time__gte=timezone.now()
        ).order_by("start_time")

        if category:
            events = events.filter(category=category)
        if event_type:
            events = events.filter(type=event_type)
        if tags:  # Assuming tags is a JSONField containing a list
            events = events.filter(tags__contains=tags)


        events = events.order_by("start_datetime")  # Order by date

        # Apply pagination (Only for this view)
        paginator = self.CustomPaginator()
        paginated_events = paginator.paginate_queryset(events, request)

        return paginator.get_paginated_response(
            {
                "events": [
                    {
                        "details": EventSerializer(event).details_serializer(),
                        "has_liked": models.EventInteractions.objects.filter(
                            event=event, user=request.user, interaction_type="like"
                        ).exists(),
                        "rsvped": models.EventAttendees.objects.filter(
                            event=event, user=request.user
                        ).exists(),
                        "attended": models.EventAttendees.objects.filter(
                            event=event, user=request.user, is_present=True
                        ).exists(),
                    }
                    for event in paginated_events
                ]
            },
            status=status.HTTP_200_OK,
        )


class EventInteractionAPI(APIView):
    """API view to interact with events

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to interact with events

        Input Serializer:
            - event_id
            - action

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
                - Event not found (event_id field)
                - Invalid action (action field)
            - Successes
                - success message
        """

        event_id = request.data.get("event_id")
        action = request.data.get("action")

        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if action == "comment":
            models.EventInteractions.objects.create(
                event=event,
                user=request.user,
                interaction_type="comment",
                interaction_data={"comment": request.data.get("comment")},
            )
        elif action == "share":
            models.EventInteractions.objects.get_or_create(
                event=event,
                user=request.user,
                interaction_type="share",
                interaction_data={},
            )
        else:
            return Response(
                {"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"success": "Action performed"}, status=status.HTTP_200_OK)


class EventRSVPAPI(APIView):
    """API view to RSVP for events

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to RSVP for events

        Input Serializer:
            - event_id

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
                - Event not found (event_id field)
            - Successes
                - success message
        """

        event_id = request.data.get("event_id")

        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        models.EventAttendees.objects.get_or_create(
            event=event,
            user=request.user,
        )

        return Response({"success": "RSVP done"}, status=status.HTTP_200_OK)


class EventRemoveRSVPAPI(APIView):
    """API view to remove RSVP for events

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to remove RSVP for events

        Input Serializer:
            - event_id

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
                - Event not found (event_id field)
            - Successes
                - success message
        """

        event_id = request.data.get("event_id")

        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        models.EventAttendees.objects.filter(
            event=event,
            user=request.user,
        ).delete()

        return Response({"success": "RSVP removed"}, status=status.HTTP_200_OK)


class EventListByOrganisation(APIView):
    """API view to listing events under an organisation

    Methods:
        GET
    """

    permission_classes = []

    def get(self, request, organisation_id: int):
        """GET Method to fetch events feed

        Output Serializer:
            - EventSerializer

        Possible Outputs:
            - Errors
                - Permission Denied (if user not part of org)
            - Successes
                - events feed of organisation
        """
        if not OrganisationCommittee.objects.filter(
            organisation__id=organisation_id, user=request.user
        ).exists():
            return Response(
                {"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        events = models.Event.objects.filter(
            start_time__gte=timezone.now(), organisation__id=organisation_id
        ).order_by("start_time")

        return Response(
            {
                "events": [
                    {
                        "details": EventSerializer(event).details_serializer(),
                    }
                    for event in events
                ]
            },
            status=status.HTTP_200_OK,
        )


# ! CSV Import for creation and updation


class EventAttendeeList(APIView):
    """API view to list attendees of an event

    Methods:
        GET
    """

    permission_classes = []

    def get(self, request, event_id: int):
        """GET Method to fetch event attendees

        Output Serializer:
            - AttendeeSerializer

        Possible Outputs:
            - Errors
                - Event not found (event_id field)
            - Successes
                - attendees list
        """

        if not OrganisationCommittee.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        attendees = models.EventAttendees.objects.filter(event=event)

        return Response(
            {
                "attendees": [
                    {
                        "user": UserSerializer(attendee).condensed_details_serializer(),
                        "is_present": attendee.is_present,
                    }
                    for attendee in attendees
                ]
            },
            status=status.HTTP_200_OK,
        )


class EventGetScanID(APIView):
    """API view to get scan ID for generating QR

    Methods:
        GET
    """

    permission_classes = []

    def get(self, request, event_id: int):
        """GET Method to fetch scan ID for generating QR

        Output Serializer:
            - scan_id

        Possible Outputs:
            - Errors
                - Event not found (event_id field)
            - Successes
                - scan_id
        """

        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if not OrganisationCommittee.objects.filter(
            organisation=event.organisation, user=request.user
        ).exists():
            return Response(
                {"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        return Response({"scan_id": event.scan_id}, status=status.HTTP_200_OK)


class EventMarkPresent(APIView):
    """API view to mark an attendee as present

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to mark an attendee as present

        Input Serializer:
            - event_id
            - scan_id

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
                - Event not found (event_id field)
                - Attendee not found (scan_id field)
            - Successes
                - success message
        """

        event_id = request.data.get("event_id")
        scan_id = request.data.get("scan_id")

        event = models.Event.objects.filter(id=event_id, scan_id=scan_id).first()

        if not event:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        attendee = models.EventAttendees.objects.filter(
            event=event, attendee=request.user
        ).first()

        if not attendee:
            return Response(
                {"error": "Attendee not found"}, status=status.HTTP_404_NOT_FOUND
            )

        attendee.is_present = True
        attendee.save()

        return Response(
            {"success": "Attendee marked as present"}, status=status.HTTP_200_OK
        )
