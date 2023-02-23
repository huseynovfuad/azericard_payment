from django.shortcuts import HttpResponse
from .azericard import Azericard

# Create your views here.


def index_view(request):
    azericard = Azericard()
    response = azericard.get_payment_page(
        total_price=0.01, order_id="101011", description="test-payment", currency="AZN"
    )
    return HttpResponse(response)