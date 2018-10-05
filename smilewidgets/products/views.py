from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from djangorestframework_camel_case.util import underscoreize

from .serializers import GetPriceSerializer
from .models import ProductPrice


class GetPrice(APIView):
    def get(self, request):
        product = None
        gift_card = None

        try:
            serializer = GetPriceSerializer(data=underscoreize(request.query_params))
            serializer.is_valid(raise_exception=True)

            gift_card = serializer.validated_data.get('gift_card')
            product = serializer.validated_data['product']
            date = serializer.validated_data['date']

            product_price = ProductPrice.objects.get(
                Q(date_end__gte=date) | Q(date_end=None),
                date_start__lte=date,
                product=product.id,
            )

            price = product_price.amount
        except ProductPrice.DoesNotExist:
            # If there is no price for given date use default price
            price = product.price
        except GetPriceSerializer.ValidationError as validation_error:
            date_errors = validation_error.detail.get('date', [None]).pop()
            other_fields_errors = validation_error.detail.get('non_field_errors', [None]).pop()

            return Response({
                'error': other_fields_errors if other_fields_errors else date_errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if gift_card is not None:
            price = max(price - gift_card.amount, 0)

        return Response(price)
