import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/prayer_request_model.dart';

class PrayerService {
  Future<List<PrayerRequestModel>> fetchRequests() async {
    final response = await ApiClient.instance.get(ApiConfig.prayerRequests);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => PrayerRequestModel.fromJson(e)).toList();
  }

  Future<bool> submitRequest({required String body, required bool isAnonymous}) async {
    final response = await ApiClient.instance.post(
      ApiConfig.prayerRequests,
      body: {'body': body, 'is_anonymous': isAnonymous},
    );
    return response.statusCode == 201;
  }

  Future<bool> markSupporting(String requestId) async {
    final response = await ApiClient.instance.post('${ApiConfig.prayerRequests}$requestId/support/');
    return response.statusCode == 200 || response.statusCode == 201;
  }
}
