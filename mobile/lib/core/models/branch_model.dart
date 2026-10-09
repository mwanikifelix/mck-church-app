/// Mirrors apps.accounts.serializers.BranchSerializer exactly.
class BranchModel {
  final String id;
  final String name;
  final String address;
  final double? latitude;
  final double? longitude;
  final int attendanceRadiusMeters;

  BranchModel({
    required this.id,
    required this.name,
    required this.address,
    this.latitude,
    this.longitude,
    required this.attendanceRadiusMeters,
  });

  factory BranchModel.fromJson(Map<String, dynamic> json) {
    return BranchModel(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      address: json['address'] ?? '',
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
      attendanceRadiusMeters: json['attendance_radius_meters'] ?? 100,
    );
  }
}
