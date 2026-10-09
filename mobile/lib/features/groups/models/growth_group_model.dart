/// Mirrors apps.groups.serializers.GroupSerializer.
class GrowthGroupModel {
  final String id;
  final String name;
  final String description;
  final int minAge;
  final int maxAge;
  final String maritalStatusRequirement;
  final bool enforceEligibility;
  final bool hasStages;
  final int memberTotal;

  GrowthGroupModel({
    required this.id,
    required this.name,
    required this.description,
    required this.minAge,
    required this.maxAge,
    required this.maritalStatusRequirement,
    required this.enforceEligibility,
    required this.hasStages,
    required this.memberTotal,
  });

  factory GrowthGroupModel.fromJson(Map<String, dynamic> json) {
    return GrowthGroupModel(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      minAge: json['min_age'] ?? 0,
      maxAge: json['max_age'] ?? 120,
      maritalStatusRequirement: json['marital_status_requirement'] ?? 'any',
      enforceEligibility: json['enforce_eligibility'] ?? false,
      hasStages: json['has_stages'] ?? false,
      memberTotal: json['member_total'] ?? 0,
    );
  }
}
