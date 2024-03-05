from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person, CarAd
from .serializers import PersonSerializer, PersonPostSerializer, CarAdSerializer, NotificationSerializer
from .services.crawler import fetch_from_bama
from .services.notification import send_email
from django.core.cache import cache


#### Person ####
class PersonView(APIView):
    """
    A view for handling operations related to Person objects.
    """
    def get(self, request):
        """
        Retrieves all Person objects.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: A response object containing serialized data of all Person objects.
        """
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new Person object.

        Args:
            request (rest_framework.request.Request): The request object containing the data for creating a new Person object.

        Returns:
            rest_framework.response.Response: A response object. If the request data is valid, it returns the serialized data of the created Person object and HTTP 201 Created status. If the request data is not valid, it returns the serializer errors and HTTP 400 Bad Request status.
        """
        serializer = PersonPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonDetailView(APIView):
    """
    A view for handling operations related to a specific Person object.
    """
    def get_object(self, id):
        """
        Retrieves a specific Person object.

        Args:
            id (int): The id of the Person object.

        Returns:
            rest_framework.response.Response: A response object. If the Person object exists, it returns the Person object. If the Person object does not exist, it returns HTTP 404 Not Found status.
        """
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        """
        Retrieves a specific Person object.

        Args:
            request (rest_framework.request.Request): The request object.
            id (int): The id of the Person object.

        Returns:
            rest_framework.response.Response: A response object containing the serialized data of the Person object.
        """
        person = self.get_object(id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, id):
        """
        Updates a specific Person object.

        Args:
            request (rest_framework.request.Request): The request object containing the data for updating the Person object.
            id (int): The id of the Person object.

        Returns:
            rest_framework.response.Response: A response object. If the request data is valid, it returns the serialized data of the updated Person object. If the request data is not valid, it returns the serializer errors and HTTP 400 Bad Request status.
        """
        person = self.get_object(id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Deletes a specific Person object.

        Args:
            request (rest_framework.request.Request): The request object.
            id (int): The id of the Person object.

        Returns:
            rest_framework.response.Response: A response object with HTTP 204 No Content status.
        """
        person = self.get_object(id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#### CarAds #####

class CarAdView(APIView):
    """
    A view for handling operations related to CarAd objects.
    """
    def get(self, request):
        """
        Retrieves all CarAd objects.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: A response object containing serialized data of all CarAd objects.
        """
        car_ads = CarAd.objects.all()
        serializer = CarAdSerializer(car_ads, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new CarAd object.

        Args:
            request (rest_framework.request.Request): The request object containing the data for creating a new CarAd object.

        Returns:
            rest_framework.response.Response: A response object. If the request data is valid, it returns the serialized data of the created CarAd object and HTTP 201 Created status. If the request data is not valid, it returns the serializer errors and HTTP 400 Bad Request status.
        """
        serializer = CarAdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarAdDetailView(APIView):
    """
    A view for handling operations related to a specific CarAd object.
    """
    def get_object(self, id):
        try:
            return CarAd.objects.get(id=id)
        except CarAd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        """
        Retrieves a specific CarAd object.

        Args:
            request (rest_framework.request.Request): The request object.
            id (int): The id of the CarAd object.

        Returns:
            rest_framework.response.Response: A response object containing the serialized data of the CarAd object.
        """
        car_ad = self.get_object(id)
        serializer = CarAdSerializer(car_ad)
        return Response(serializer.data)

    def put(self, request, id):
        """
        Updates a specific CarAd object.

        Args:
            request (rest_framework.request.Request): The request object containing the data for updating the CarAd object.
            id (int): The id of the CarAd object.

        Returns:
            rest_framework.response.Response: A response object. If the request data is valid, it returns the serialized data of the updated CarAd object. If the request data is not valid, it returns the serializer errors and HTTP 400 Bad Request status.
        """
        car_ad = self.get_object(id)
        serializer = CarAdSerializer(car_ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Deletes a specific CarAd object.

        Args:
            request (rest_framework.request.Request): The request object.
            id (int): The id of the CarAd object.

        Returns:
            rest_framework.response.Response: A response object with HTTP 204 No Content status.
        """
        car_ad = self.get_object(id)
        car_ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#### CarAds #####

class CrawlView(APIView):
    """
    A view for handling operations related to crawling car ads.
    """

    def post(self, request):
        """
        Crawls car ads based on a specific state.

        Args:
            request (rest_framework.request.Request): The request object containing the state for crawling car ads.

        Returns:
            rest_framework.response.Response: A response object. The response depends on the status code of the crawling operation.
        """
        data = request.data
        state = data["state"]
        ads_data = fetch_from_bama(state)
        ads_status_code = ads_data["status"]
        ads_reason = ads_data["reason"]
        ads = ads_data["ads"]
        if ads_status_code == 200:
            new_ads = []
            for ad in ads.values():
                if not cache.get(ad['code']):  # If the ad is not in Redis, it's a new ad
                    cache.set(ad['code'], True, timeout=None)  # Add the new ad's code to Redis
                    new_ads.append(ad)  # Add the new ad to the new_ads list

                    # Create a new CarAd instance and save it to the database
                    car_ad = CarAd(**ad)
                    car_ad.save()

            if new_ads:  # If there are new ads
                serializer = CarAdSerializer(new_ads, many=True)  # Serialize only the new ads
                return Response({"message": "New ads have been added!", "ads": serializer.data, "new": True }, status=200)
            else:
                return Response({"message": "No new ads found.",  "new": False})
        elif ads_status_code == 408:
            return Response({"error": "Request Timeout",  "new": False}, status=408)
        elif ads_status_code == 503:
            return Response({"error": "Connection Timeout",  "new": False}, status=503)
        else:
            return Response({"error": "An error occurred",  "new": False}, status=500)


#### notification #####

class SendNotificationView(APIView):
    """
    A view for handling operations related to send email notification.
    """
    def post(self, request):
        """
        Sends a notification email to all persons in the database.

        Args:
            request (rest_framework.request.Request): 
            The request object that contains all the data for sending the notification. 
            The data should include 'state', 'url', 'title', 'year', 'mileage', 'price'.

        Returns:
            rest_framework.response.Response: 
            A response object. If the request data is valid, it returns a success message and HTTP 200 OK status.
            If the request data is not valid, it returns the serializer errors and HTTP 400 Bad Request status.
        """
        
        """
        {
            "state": "string",
            "url": "string",
            "title": "string",
            "year": "integer",
            "mileage": "integer",
            "price": "decimal"
        }

        """
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            recipients = Person.objects.all().values_list('email', flat=True)
            data = serializer.validated_data
            state = data["state"]
            url = data["url"]
            title = data["title"]
            year = data["year"]
            mileage = data["mileage"]
            price = data["price"]
            for email in recipients:
                send_email(state, url, title, year, mileage, price, email)
            return Response({"message": "Emails sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
