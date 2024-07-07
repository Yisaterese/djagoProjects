from django.urls import path, include
from rest_framework.routers import SimpleRouter

from account import views

# user routers to route the useSet
# register the
router = SimpleRouter()
router.register('accounts', views.AccountViewSet)
router.register("transfer", views.TransferViewSet, basename='transfer')

urlpatterns = [
    path('', include(router.urls)),
    # comment them after you have route them
    # path('accounts', views.ListAccount.as_view()),
    # path('account/<str:pk>', views.AccountDetails.as_view()),
    # path('deposit', views.deposit),
    path('deposit',views.Deposit.as_view()),
    path('withdraw', views.Withdraw.as_view()),
    path('check_balance',views.CheckBalance.as_view()),
    #becausee you are using apiView, you  have to specify the path
#    path("createAccount",views.CreateAccount.as_view())

]
