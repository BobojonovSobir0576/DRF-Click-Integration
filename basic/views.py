from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from basic import serializers
from basic.models import ClickOrder
from pyclick import PyClick
from pyclick.views import PyClickMerchantAPIView


class CreateClickOrderView(CreateAPIView):
    serializer_class = serializers.ClickOrderSerializer

    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount')
        order = ClickOrder.objects.create(amount=amount)
        return_url = 'http://t.lemix.uz/finance/fnc'
        print(return_url)
        url = PyClick.generate_url(order_id=order.id, amount=str(amount), return_url=return_url)
        print()
        print(url)
        return redirect(url)


class OrderCheckAndPayment(PyClick):
    def check_order(self, order_id: str, amount: str):
        print(order_id,amount)
        if order_id:
            try:
                order = ClickOrder.objects.get(id=order_id)
                if int(amount) == order.amount:
                    return self.ORDER_FOUND
                else:
                    return self.INVALID_AMOUNT
            except ClickOrder.DoesNotExist:
                return self.ORDER_NOT_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        """ Эта функция вызывается после успешной оплаты """
        try:
            order = ClickOrder.objects.get(id=order_id)
            order.is_paid = True
            order.save()
        except ClickOrder.DoesNotExist:
            print(f"no order object not found: {order_id}")


class OrderTestView(PyClickMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment