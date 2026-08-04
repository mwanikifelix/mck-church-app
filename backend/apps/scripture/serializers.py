from rest_framework import serializers

from .models import BibleBook, BibleVerse, BibleVersion, Hymn, HymnFile


class BibleVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleVersion
        fields = ["id", "code", "name", "language", "is_public_domain"]


class BibleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleBook
        fields = ["id", "name", "abbreviation", "testament", "order"]


class BibleVerseSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.name", read_only=True)
    version_code = serializers.CharField(source="version.code", read_only=True)

    class Meta:
        model = BibleVerse
        fields = ["id", "version", "version_code", "book", "book_name", "chapter", "verse_number", "text"]


class HymnFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HymnFile
        fields = ["id", "hymn", "file_type", "file", "text_content", "branch", "uploaded_by", "updated_at"]
        read_only_fields = ["id", "uploaded_by", "updated_at"]


class HymnSerializer(serializers.ModelSerializer):
    file = HymnFileSerializer(read_only=True)

    class Meta:
        model = Hymn
        fields = ["id", "number", "title", "first_line", "file"]
