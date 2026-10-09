import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/donation_model.dart';
import '../models/paybill_model.dart';

class GivingService {
  Future<List<DonationModel>> fetchMyDonations() async {
    final response = await ApiClient.instance.get(ApiConfig.myDonations);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => DonationModel.fromJson(e)).toList();
  }

  Future<PaybillModel?> fetchPaybill() async {
    final response = await ApiClient.instance.get(ApiConfig.paybill);
    if (response.statusCode != 200) return null;
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    if (list is List && list.isNotEmpty) return PaybillModel.fromJson(list.first);
    return null;
  }

  /// Records a self-reported gift. Matches apps.giving.views.DonationViewSet
  /// — the requester is always set as `member` server-side, so no user
  /// field is sent from here.
  Future<void> recordDonation({
    required String accountCode,
    required double amount,
    String? phone,
    String? mpesaRef,
    String? description,
  }) async {
    final response = await ApiClient.instance.post(
      ApiConfig.donations,
      body: {
        'account_code': accountCode,
        'amount': amount,
        if (phone != null) 'phone': phone,
        if (mpesaRef != null) 'mpesa_ref': mpesaRef,
        if (description != null) 'description': description,
      },
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to record donation (${response.statusCode})');
    }
  }
}
