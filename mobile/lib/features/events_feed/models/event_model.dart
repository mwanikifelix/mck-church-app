/// Mirrors apps.events.serializers.EventSerializer.
class EventModel {
  final String id;
  final String title;
  final String description;
  final String location;
  final DateTime startTime;
  final DateTime? endTime;
  final String? departmentName;
  final String? hbcGroupName;
  final int rsvpCount;

  EventModel({
    required this.id,
    required this.title,
    required this.description,
    required this.location,
    required this.startTime,
    this.endTime,
    this.departmentName,
    this.hbcGroupName,
    required this.rsvpCount,
  });

  factory EventModel.fromJson(Map<String, dynamic> json) {
    return EventModel(
      id: json['id'].toString(),
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      location: json['location'] ?? '',
      startTime: DateTime.parse(json['start_time']),
      endTime: json['end_time'] != null ? DateTime.parse(json['end_time']) : null,
      departmentName: json['department_name'],
      hbcGroupName: json['hbc_group_name'],
      rsvpCount: json['rsvp_count'] ?? 0,
    );
  }
}
