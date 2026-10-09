import 'branch_model.dart';
import 'role_model.dart';

/// Mirrors apps.accounts.serializers.UserSerializer exactly. No `phone`
/// field exists on the backend User model — do not add one here without
/// also adding it on the Django side first.
class UserModel {
  final String id;
  final String email;
  final String fullName;
  final String? passportPhoto; // full URL from Django's MEDIA_URL
  final String membershipNumber;
  final BranchModel? branch;
  final RoleModel? role;
  final String? dateOfBirth; // ISO date string, e.g. "1998-04-12"
  final String? maritalStatus; // single | married | widowed | divorced
  final String status; // active | inactive | transferred
  final int? age; // server-computed from date_of_birth
  final List<String> visibleFolders; // role-driven home screen sections
  final String dateJoined; // ISO datetime string

  UserModel({
    required this.id,
    required this.email,
    required this.fullName,
    this.passportPhoto,
    required this.membershipNumber,
    this.branch,
    this.role,
    this.dateOfBirth,
    this.maritalStatus,
    required this.status,
    this.age,
    required this.visibleFolders,
    required this.dateJoined,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'].toString(),
      email: json['email'] ?? '',
      fullName: json['full_name'] ?? '',
      passportPhoto: json['passport_photo'],
      membershipNumber: json['membership_number'] ?? '',
      branch: json['branch'] != null ? BranchModel.fromJson(json['branch']) : null,
      role: json['role'] != null ? RoleModel.fromJson(json['role']) : null,
      dateOfBirth: json['date_of_birth'],
      maritalStatus: json['marital_status'],
      status: json['status'] ?? 'active',
      age: json['age'] is int ? json['age'] as int : null,
      visibleFolders: (json['visible_folders'] as List<dynamic>? ?? [])
          .map((e) => e.toString())
          .toList(),
      dateJoined: json['date_joined'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'email': email,
        'full_name': fullName,
        'passport_photo': passportPhoto,
        'membership_number': membershipNumber,
        'branch': branch == null
            ? null
            : {
                'id': branch!.id,
                'name': branch!.name,
                'address': branch!.address,
                'latitude': branch!.latitude,
                'longitude': branch!.longitude,
                'attendance_radius_meters': branch!.attendanceRadiusMeters,
              },
        'role': role == null
            ? null
            : {
                'id': role!.id,
                'name': role!.name,
                'is_admin': role!.isAdmin,
                'can_act_as_superintendent': role!.canActAsSuperintendent,
                'is_clergy': role!.isClergy,
                'permissions': role!.permissions,
              },
        'date_of_birth': dateOfBirth,
        'marital_status': maritalStatus,
        'status': status,
        'age': age,
        'visible_folders': visibleFolders,
        'date_joined': dateJoined,
      };

  bool get isSuperuser => role?.isAdmin == true && role?.name == 'System Admin';
  bool hasPermission(String code) => role?.hasPermission(code) ?? false;
}
