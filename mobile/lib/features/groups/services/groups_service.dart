import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/department_model.dart';
import '../models/growth_group_model.dart';
import '../models/hbc_group_model.dart';

class GroupsService {
  List<T> _extractList<T>(String body, T Function(Map<String, dynamic>) fromJson) {
    final data = jsonDecode(body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => fromJson(e as Map<String, dynamic>)).toList();
  }

  // --- Growth-track (JCTM / Youth / Main Church) ---
  Future<List<GrowthGroupModel>> fetchGrowthGroups() async {
    final response = await ApiClient.instance.get(ApiConfig.growthGroups);
    if (response.statusCode != 200) return [];
    return _extractList(response.body, GrowthGroupModel.fromJson);
  }

  /// Direct join — eligibility (age/marital status) is checked
  /// server-side; a 400 response means the member doesn't qualify.
  Future<String?> joinGrowthGroup(String groupId) async {
    final response = await ApiClient.instance.post('${ApiConfig.growthGroups}$groupId/join/');
    if (response.statusCode == 201 || response.statusCode == 200) return null;
    try {
      final data = jsonDecode(response.body);
      return data is Map ? (data['detail']?.toString() ?? 'Could not join this group.') : 'Could not join this group.';
    } catch (_) {
      return 'Could not join this group.';
    }
  }

  // --- Departments (join-request, needs approval) ---
  Future<List<DepartmentModel>> fetchDepartments() async {
    final response = await ApiClient.instance.get(ApiConfig.departments);
    if (response.statusCode != 200) return [];
    return _extractList(response.body, DepartmentModel.fromJson);
  }

  Future<bool> requestDepartmentJoin(String departmentId, {String message = ''}) async {
    final response = await ApiClient.instance.post(
      '${ApiConfig.departments}$departmentId/join/',
      body: {'message': message},
    );
    return response.statusCode == 201;
  }

  // --- HBC (direct join) ---
  Future<List<HbcGroupModel>> fetchHbcGroups() async {
    final response = await ApiClient.instance.get(ApiConfig.hbcGroups);
    if (response.statusCode != 200) return [];
    return _extractList(response.body, HbcGroupModel.fromJson);
  }

  Future<HbcGroupModel?> fetchMyHbc() async {
    final response = await ApiClient.instance.get(ApiConfig.myHbc);
    if (response.statusCode != 200) return null;
    return HbcGroupModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<bool> joinHbc(String hbcId) async {
    final response = await ApiClient.instance.post('${ApiConfig.hbcGroups}$hbcId/join/');
    return response.statusCode == 200 || response.statusCode == 201;
  }
}
