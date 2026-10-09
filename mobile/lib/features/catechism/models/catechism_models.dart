/// Mirrors apps.registration.serializers.RegistrationWindowSerializer.
class RegistrationWindowModel {
  final String id;
  final String name;
  final String description;
  final DateTime opensAt;
  final DateTime closesAt;
  final bool isOpen;

  RegistrationWindowModel({
    required this.id,
    required this.name,
    required this.description,
    required this.opensAt,
    required this.closesAt,
    required this.isOpen,
  });

  factory RegistrationWindowModel.fromJson(Map<String, dynamic> json) {
    return RegistrationWindowModel(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      opensAt: DateTime.parse(json['opens_at']).toLocal(),
      closesAt: DateTime.parse(json['closes_at']).toLocal(),
      isOpen: json['is_open'] ?? false,
    );
  }
}

/// Mirrors apps.registration.serializers.CatechismRegistrationSerializer.
class CatechismRegistrationModel {
  final String id;
  final String windowId;
  final String windowName;
  final String status; // pending | confirmed | completed
  final DateTime submittedAt;

  CatechismRegistrationModel({
    required this.id,
    required this.windowId,
    required this.windowName,
    required this.status,
    required this.submittedAt,
  });

  factory CatechismRegistrationModel.fromJson(Map<String, dynamic> json) {
    return CatechismRegistrationModel(
      id: json['id'].toString(),
      windowId: json['window'].toString(),
      windowName: json['window_name'] ?? '',
      status: json['status'] ?? 'pending',
      submittedAt: DateTime.parse(json['submitted_at']).toLocal(),
    );
  }
}
