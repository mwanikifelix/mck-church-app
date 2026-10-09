/// Mirrors apps.pastoral.serializers.ClergyDirectoryEntrySerializer.
class ClergyModel {
  final String id;
  final String fullName;
  final String title; // derived from the person's Role name
  final String? photoUrl;
  final String? branchName;

  ClergyModel({
    required this.id,
    required this.fullName,
    required this.title,
    this.photoUrl,
    this.branchName,
  });

  factory ClergyModel.fromJson(Map<String, dynamic> json) {
    return ClergyModel(
      id: json['id'].toString(),
      fullName: json['full_name'] ?? '',
      title: json['title'] ?? '',
      photoUrl: json['passport_photo'],
      branchName: json['branch_name'],
    );
  }
}
