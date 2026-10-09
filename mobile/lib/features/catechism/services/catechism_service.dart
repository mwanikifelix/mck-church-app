import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/catechism_models.dart';

class CatechismService {
  List<T> _list<T>(String body, T Function(Map<String, dynamic>) fromJson) {
    final data = jsonDecode(body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => fromJson(e as Map<String, dynamic>)).toList();
  }

  Future<List<RegistrationWindowModel>> fetchWindows() async {
    final response = await ApiClient.instance.get(ApiConfig.registrationWindows);
    if (response.statusCode != 200) throw Exception('windows ${response.statusCode}');
    return _list(response.body, RegistrationWindowModel.fromJson);
  }

  Future<List<CatechismRegistrationModel>> fetchMyRegistrations() async {
    final response = await ApiClient.instance.get(ApiConfig.catechismRegistrations);
    if (response.statusCode != 200) throw Exception('registrations ${response.statusCode}');
    return _list(response.body, CatechismRegistrationModel.fromJson);
  }

  /// Returns null on success, or an error message to show the member.
  /// The server enforces the open/close window, so a 400 here usually
  /// means the window closed or the member already registered.
  Future<String?> register(String windowId) async {
    final response = await ApiClient.instance.post(
      ApiConfig.catechismRegistrations,
      body: {'window': windowId},
    );
    if (response.statusCode == 201) return null;
    try {
      final data = jsonDecode(response.body);
      if (data is Map) {
        final first = data.values.first;
        return first is List ? first.join(', ') : first.toString();
      }
    } catch (_) {}
    return 'Could not register. Please try again.';
  }
}
