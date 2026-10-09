/// Mirrors apps.scripture.serializers.HymnSerializer.
class HymnModel {
  final String id;
  final int number;
  final String title;
  final String firstLine;
  final String? fileType;
  final String? fileUrl;

  HymnModel({
    required this.id,
    required this.number,
    required this.title,
    required this.firstLine,
    this.fileType,
    this.fileUrl,
  });

  factory HymnModel.fromJson(Map<String, dynamic> json) {
    final file = json['file'] as Map<String, dynamic>?;
    return HymnModel(
      id: json['id'].toString(),
      number: json['number'] ?? 0,
      title: json['title'] ?? '',
      firstLine: json['first_line'] ?? '',
      fileType: file?['file_type'],
      fileUrl: file?['file'],
    );
  }
}
