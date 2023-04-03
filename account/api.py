from . import views
from server.routers import CustomRouter
from rest_framework_nested import routers

custom = CustomRouter()
router = routers.SimpleRouter()

custom.register("user", views.UserAPI, "user")
router.register("user/notes", views.NoteAPI, "user-notes")
router.register("resend", views.PasscodeResendAPI, "resend")
router.register("verify", views.PasscodeActivateAPI, "verify")
custom.register("user/profile", views.ProfileAPI, "user-profile")
custom.register("user/settings", views.SettingsAPI, "user-settings")
custom.register("reset-password", views.PasswordResetAPI, "reset-password")
custom.register("change-password", views.PasswordChangeAPI, "change-password")


urlpatterns = custom.urls + router.urls
