import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/counselling_request_model.dart';

class CounsellingService {
  Future<List<CounsellingRequestModel>> fetchMine() async {
    final response = await ApiClient.instance.get(ApiConfig.counsellingRequests);
    if (response.statusCode != 200) throw Exception('counselling ${response.statusCode}');
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => CounsellingRequestModel.fromJson(e)).toList();
  }

  /// Open request flow: the member only describes what they need. A
  /// counsellor confirms and sets the date/time on the admin side.
  Future<bool> submit(String message) async {
    final response = await ApiClient.instance.post(
      ApiConfig.counsellingRequests,
      body: {'message': message},
    );
    return response.statusCode == 201;
  }

  Future<bool> cancel(String id) async {
    final response = await ApiClient.instance.patch(
      '${ApiConfig.counsellingRequests}$id/',
      body: {'status': 'cancelled'},
    );
    return response.statusCode == 200;
  }
}
