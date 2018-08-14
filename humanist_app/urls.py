from django.urls import path

# Legacy views
from .views import (UserView, UserLogoutView, UserUpdateView,
                    UserUnsubscribeView, UserUnsubscribeConfirmView,
                    WebResetPasswordView,
                    WebAnnouncementView,
                    WebHomepageView, WebLogin, WebRestrictedDeniedView,
                    WebQuackView, WebMembershipFormView,
                    WebForgottenPasswordForm)

urlpatterns = [
    # These are the legacy website, which we have not changed
    path('', WebHomepageView.as_view()),
    path('announcement.html', WebAnnouncementView.as_view()),
    path('quack.html', WebQuackView.as_view()),
    path('Restricted/', WebLogin.as_view()),
    path('Restricted/denied/', WebRestrictedDeniedView.as_view()),

    path('membership_form.php', WebMembershipFormView.as_view()),
    path('forgot_password.php', WebForgottenPasswordForm.as_view()),
    path('user/reset/', WebResetPasswordView.as_view()),

    # User Pages
    path('user/', UserView.as_view()),
    path('user/logout/', UserLogoutView.as_view()),
    path('user/update/', UserUpdateView.as_view()),
    path('user/unsubscribe/', UserUnsubscribeView.as_view()),
    path('user/unsubscribe/confirm/', UserUnsubscribeConfirmView.as_view()),


    # Editor Pages
    path('editor/logout/', UserLogoutView.as_view()),

]
