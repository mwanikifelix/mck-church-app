/// Mirrors apps.content.serializers.LivestreamSerializer.
class LivestreamModel {
  final String id;
  final String title;
  final String platform;
  final String url;
  final bool isLive;
  final DateTime? scheduledFor;

  LivestreamModel({
    required this.id,
    required this.title,
    required this.platform,
    required this.url,
    required this.isLive,
    this.scheduledFor,
  });

  factory LivestreamModel.fromJson(Map<String, dynamic> json) {
    return LivestreamModel(
      id: json['id'].toString(),
      title: json['title'] ?? '',
      platform: json['platform'] ?? '',
      url: json['url'] ?? '',
      isLive: json['is_live'] ?? false,
      scheduledFor: json['scheduled_for'] != null ? DateTime.parse(json['scheduled_for']) : null,
    );
  }
}
