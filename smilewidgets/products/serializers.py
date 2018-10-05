from rest_framework import serializers


from .models import Product, GiftCard


class GetPriceSerializer(serializers.Serializer):
    ValidationError = serializers.ValidationError

    product_code = serializers.CharField()
    date = serializers.DateField()
    gift_card_code = serializers.CharField(required=False)

    def validate(self, attrs):
        product_code = attrs['product_code']
        gift_card_code = attrs.get('gift_card_code')
        date = attrs['date']

        try:
            product = Product.objects.get(code=product_code)
            gift_card = GiftCard.objects.get(code=gift_card_code) if gift_card_code else None
        except Product.DoesNotExist:
            raise serializers.ValidationError('No such product')
        except GiftCard.DoesNotExist:
            raise serializers.ValidationError('No such gift card')

        if gift_card and not gift_card.is_valid(date):
            raise serializers.ValidationError('Invalid gift card')

        return {
            'product': product,
            'gift_card': gift_card,
            'date': date
        }
