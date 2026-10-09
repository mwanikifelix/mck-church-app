/// Mirrors apps.church.serializers.DepartmentSerializer.
class DepartmentModel {
  final String id;
  final String name;
  final String description;
  final String? leaderName;
  final String meetingDay;
  final String meetingTime;
  final int memberCount;

  DepartmentModel({
    required this.id,
    required this.name,
    required this.description,
    this.leaderName,
    required this.meetingDay,
    required this.meetingTime,
    required this.memberCount,
  });

  factory DepartmentModel.fromJson(Map<String, dynamic> json) {
    return DepartmentModel(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      leaderName: json['leader_name'],
      meetingDay: json['meeting_day'] ?? '',
      meetingTime: json['meeting_time'] ?? '',
      memberCount: json['member_count'] ?? 0,
    );
  }
}
