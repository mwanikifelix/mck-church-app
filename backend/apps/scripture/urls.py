from rest_framework.routers import DefaultRouter

from .views import BibleBookViewSet, BibleVerseViewSet, BibleVersionViewSet, HymnFileViewSet, HymnViewSet

router = DefaultRouter()
router.register("bible/versions", BibleVersionViewSet, basename="bible-version")
router.register("bible/books", BibleBookViewSet, basename="bible-book")
router.register("bible/verses", BibleVerseViewSet, basename="bible-verse")
router.register("hymns", HymnViewSet, basename="hymn")
router.register("hymn-files", HymnFileViewSet, basename="hymn-file")

urlpatterns = router.urls
