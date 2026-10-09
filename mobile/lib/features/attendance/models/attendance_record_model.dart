/// Mirrors apps.attendance.serializers.AttendanceRecordSerializer.
class AttendanceRecordModel {
  final String id;
  final String branchName;
  final DateTime date;
  final DateTime checkedInAt;
  final double distanceMeters;

  AttendanceRecordModel({
    required this.id,
    required this.branchName,
    required this.date,
    required this.checkedInAt,
    required this.distanceMeters,
  });

  factory AttendanceRecordModel.fromJson(Map<String, dynamic> json) {
    return AttendanceRecordModel(
      id: json['id'].toString(),
      branchName: json['branch_name'] ?? '',
      date: DateTime.parse(json['date']),
      checkedInAt: DateTime.parse(json['checked_in_at']).toLocal(),
      distanceMeters: (json['distance_meters'] as num?)?.toDouble() ?? 0,
    );
  }
}
