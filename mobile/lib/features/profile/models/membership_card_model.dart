/// Mirrors apps.membership.serializers.MembershipCardSerializer.
class MembershipCardModel {
  final String membershipNumber;
  final String fullName;
  final String? passportPhoto;
  final String? branchName;
  final String status;
  final DateTime dateIssued;
  final List<String> departmentNames;
  final String? hbcGroupName;
  final String? growthTrackCategory;

  MembershipCardModel({
    required this.membershipNumber,
    required this.fullName,
    this.passportPhoto,
    this.branchName,
    required this.status,
    required this.dateIssued,
    required this.departmentNames,
    this.hbcGroupName,
    this.growthTrackCategory,
  });

  factory MembershipCardModel.fromJson(Map<String, dynamic> json) {
    return MembershipCardModel(
      membershipNumber: json['membership_number'] ?? '',
      fullName: json['full_name'] ?? '',
      passportPhoto: json['passport_photo'],
      branchName: json['branch_name'],
      status: json['status'] ?? 'active',
      dateIssued: DateTime.parse(json['date_issued']),
      departmentNames: (json['department_names'] as List<dynamic>? ?? []).map((e) => e.toString()).toList(),
      hbcGroupName: json['hbc_group_name'],
      growthTrackCategory: json['growth_track_category'],
    );
  }
}
