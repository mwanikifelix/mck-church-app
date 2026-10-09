/// Mirrors apps.scripture.serializers.BibleVerseSerializer.
class BibleVerseModel {
  final String bookName;
  final int chapter;
  final int verseNumber;
  final String text;

  BibleVerseModel({required this.bookName, required this.chapter, required this.verseNumber, required this.text});

  factory BibleVerseModel.fromJson(Map<String, dynamic> json) {
    return BibleVerseModel(
      bookName: json['book_name'] ?? '',
      chapter: json['chapter'] ?? 0,
      verseNumber: json['verse_number'] ?? 0,
      text: json['text'] ?? '',
    );
  }
}
