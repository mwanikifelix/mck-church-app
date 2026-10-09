/// Mirrors apps.prayer.serializers.PrayerRequestSerializer. Requests are
/// confidential by default — the API only ever returns the requester's
/// own requests (plus anyone with prayer.manage), so there is no
/// separate "mine vs all" filter needed client-side.
class PrayerRequestModel {
  final String id;
  final String? submitterName; // null if anonymous or not visible
  final bool isAnonymous;
  final String body;
  final String status; // open | answered
  final int supportCount;
  final DateTime createdAt;

  PrayerRequestModel({
    required this.id,
    this.submitterName,
    required this.isAnonymous,
    required this.body,
    required this.status,
    required this.supportCount,
    required this.createdAt,
  });

  factory PrayerRequestModel.fromJson(Map<String, dynamic> json) {
    return PrayerRequestModel(
      id: json['id'].toString(),
      submitterName: json['submitter_name'],
      isAnonymous: json['is_anonymous'] ?? false,
      body: json['body'] ?? '',
      status: json['status'] ?? 'open',
      supportCount: json['support_count'] ?? 0,
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
