from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import BibleBook, BibleVerse, BibleVersion, Hymn, HymnFile
from .permissions import ReadOnlyOrPermission
from .serializers import (
    BibleBookSerializer,
    BibleVerseSerializer,
    BibleVersionSerializer,
    HymnFileSerializer,
    HymnSerializer,
)


class BibleVersionViewSet(viewsets.ModelViewSet):
    queryset = BibleVersion.objects.all()
    serializer_class = BibleVersionSerializer
    permission_classes = [ReadOnlyOrPermission("ict.manage_content")]

    @action(detail=True, methods=["get"])
    def export(self, request, pk=None):
        """Bulk export — the whole version as one payload, for the
        Flutter app to cache offline. Optional ?book=<id> to scope to
        one book instead of the entire Bible."""
        version = self.get_object()
        qs = BibleVerse.objects.filter(version=version).select_related("book")
        book_id = request.query_params.get("book")
        if book_id:
            qs = qs.filter(book_id=book_id)
        return Response(BibleVerseSerializer(qs, many=True).data)


class BibleBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BibleBook.objects.all()
    serializer_class = BibleBookSerializer
    permission_classes = [IsAuthenticated]


class BibleVerseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BibleVerseSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["version", "book", "chapter"]

    def get_queryset(self):
        return BibleVerse.objects.select_related("version", "book")

    @action(detail=False, methods=["get"])
    def reference(self, request):
        """?version=KJV&book=John&chapter=3&verse=16 (verse optional —
        omit for the whole chapter)."""
        version_code = request.query_params.get("version")
        book_name = request.query_params.get("book")
        chapter = request.query_params.get("chapter")
        verse = request.query_params.get("verse")
        if not (version_code and book_name and chapter):
            return Response({"detail": "version, book, and chapter are required."}, status=400)
        qs = BibleVerse.objects.filter(
            version__code=version_code, book__name__iexact=book_name, chapter=chapter
        )
        if verse:
            qs = qs.filter(verse_number=verse)
        return Response(BibleVerseSerializer(qs, many=True).data)


class HymnViewSet(viewsets.ModelViewSet):
    queryset = Hymn.objects.select_related("file")
    serializer_class = HymnSerializer
    permission_classes = [ReadOnlyOrPermission("ict.manage_content")]
    filterset_fields = ["number"]
    search_fields = ["title", "first_line"]


class HymnFileViewSet(viewsets.ModelViewSet):
    queryset = HymnFile.objects.all()
    serializer_class = HymnFileSerializer
    permission_classes = [ReadOnlyOrPermission("ict.manage_content")]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(uploaded_by=self.request.user)
