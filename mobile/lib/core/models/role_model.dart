/// Mirrors apps.accounts.serializers.RoleSerializer exactly.
/// `permissions` is the flat list of permission codes (e.g.
/// "members.view_all") — check membership with `hasPermission(code)`.
class RoleModel {
  final String id;
  final String name;
  final bool isAdmin;
  final bool canActAsSuperintendent;
  final bool isClergy;
  final List<String> permissions;

  RoleModel({
    required this.id,
    required this.name,
    required this.isAdmin,
    required this.canActAsSuperintendent,
    required this.isClergy,
    required this.permissions,
  });

  factory RoleModel.fromJson(Map<String, dynamic> json) {
    return RoleModel(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      isAdmin: json['is_admin'] ?? false,
      canActAsSuperintendent: json['can_act_as_superintendent'] ?? false,
      isClergy: json['is_clergy'] ?? false,
      permissions: (json['permissions'] as List<dynamic>? ?? [])
          .map((e) => e.toString())
          .toList(),
    );
  }

  bool hasPermission(String code) => permissions.contains(code);
}
