/// Mirrors apps.hbc.serializers.HBCGroupSerializer.
class HbcGroupModel {
  final String id;
  final String name;
  final String location;
  final String meetingDay;
  final String meetingTime;
  final String meetingVenue;
  final String? leaderName;
  final int memberCount;

  HbcGroupModel({
    required this.id,
    required this.name,
    required this.location,
    required this.meetingDay,
    required this.meetingTime,
    required this.meetingVenue,
    this.leaderName,
    required this.memberCount,
  });

  factory HbcGroupModel.fromJson(Map<String, dynamic> json) {
    return HbcGroupModel(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      location: json['location'] ?? '',
      meetingDay: json['meeting_day'] ?? '',
      meetingTime: json['meeting_time'] ?? '',
      meetingVenue: json['meeting_venue'] ?? '',
      leaderName: json['leader_display_name'] ?? json['leader_name'],
      memberCount: json['member_count'] ?? 0,
    );
  }
}
