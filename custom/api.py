from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register("faqs", views.FaqAPI, "faqs")
router.register("categories", views.CategoryAPI, "categories")
router.register("user/galleries", views.GalleryAPI, "user-galleries")
router.register("user/notifications", views.NotificationAPI, "user-notifications")

urlpatterns = router.urls
