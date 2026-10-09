/// Mirrors apps.giving.serializers.PaybillSerializer.
class PaybillModel {
  final String number;

  PaybillModel({required this.number});

  factory PaybillModel.fromJson(Map<String, dynamic> json) {
    return PaybillModel(number: json['number'] ?? '');
  }
}
