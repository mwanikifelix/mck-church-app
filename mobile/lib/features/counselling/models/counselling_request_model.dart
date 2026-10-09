/// Mirrors apps.pastoral.serializers.CounsellingRequestSerializer.
class CounsellingRequestModel {
  final String id;
  final String message;
  final String status; // pending | confirmed | completed | cancelled
  final DateTime requestedAt;
  final DateTime? confirmedDatetime;
  final String? counsellorName;

  CounsellingRequestModel({
    required this.id,
    required this.message,
    required this.status,
    required this.requestedAt,
    this.confirmedDatetime,
    this.counsellorName,
  });

  factory CounsellingRequestModel.fromJson(Map<String, dynamic> json) {
    return CounsellingRequestModel(
      id: json['id'].toString(),
      message: json['message'] ?? '',
      status: json['status'] ?? 'pending',
      requestedAt: DateTime.parse(json['requested_at']).toLocal(),
      confirmedDatetime: json['confirmed_datetime'] != null
          ? DateTime.parse(json['confirmed_datetime']).toLocal()
          : null,
      counsellorName: json['counsellor_name'],
    );
  }
}
