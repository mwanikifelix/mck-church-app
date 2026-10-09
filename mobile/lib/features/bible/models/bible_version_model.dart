/// Mirrors apps.scripture.serializers.BibleVersionSerializer.
class BibleVersionModel {
  final String id;
  final String code;
  final String name;
  final String language;

  BibleVersionModel({required this.id, required this.code, required this.name, required this.language});

  factory BibleVersionModel.fromJson(Map<String, dynamic> json) {
    return BibleVersionModel(
      id: json['id'].toString(),
      code: json['code'] ?? '',
      name: json['name'] ?? '',
      language: json['language'] ?? '',
    );
  }
}
