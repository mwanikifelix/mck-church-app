/// Mirrors apps.giving.serializers.DonationSerializer.
class DonationModel {
  final String id;
  final String accountCode;
  final String accountCodeDisplay;
  final double amount;
  final String? mpesaRef;
  final String? description;
  final DateTime createdAt;

  DonationModel({
    required this.id,
    required this.accountCode,
    required this.accountCodeDisplay,
    required this.amount,
    this.mpesaRef,
    this.description,
    required this.createdAt,
  });

  factory DonationModel.fromJson(Map<String, dynamic> json) {
    return DonationModel(
      id: json['id'].toString(),
      accountCode: json['account_code'] ?? '',
      accountCodeDisplay: json['account_code_display'] ?? '',
      amount: double.tryParse(json['amount'].toString()) ?? 0,
      mpesaRef: json['mpesa_ref'],
      description: json['description'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
