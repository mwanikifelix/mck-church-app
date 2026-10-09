import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'api_config.dart';
import 'token_storage.dart';

/// Thrown when a request still 401s after attempting a token refresh —
/// means the refresh token itself is invalid/expired. AuthService
/// listens for this via [ApiClient.onSessionExpired] to force logout.
class SessionExpiredException implements Exception {}

/// Wraps every authenticated request with the access token, and
/// transparently refreshes + retries once on a 401 before giving up.
class ApiClient {
  ApiClient._internal();
  static final ApiClient instance = ApiClient._internal();

  void Function()? onSessionExpired;

  Future<Map<String, String>> _authHeaders({bool json = true}) async {
    final token = await TokenStorage.instance.getAccessToken();
    return {
      if (json) 'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  Future<http.Response> get(String url) => _withRefresh(
        () async => http.get(Uri.parse(url), headers: await _authHeaders(json: false)),
      );

  Future<http.Response> post(String url, {Map<String, dynamic>? body}) => _withRefresh(
        () async => http.post(
          Uri.parse(url),
          headers: await _authHeaders(),
          body: body != null ? jsonEncode(body) : null,
        ),
      );

  Future<http.Response> patch(String url, {Map<String, dynamic>? body}) => _withRefresh(
        () async => http.patch(
          Uri.parse(url),
          headers: await _authHeaders(),
          body: body != null ? jsonEncode(body) : null,
        ),
      );

  Future<http.Response> put(String url, {Map<String, dynamic>? body}) => _withRefresh(
        () async => http.put(
          Uri.parse(url),
          headers: await _authHeaders(),
          body: body != null ? jsonEncode(body) : null,
        ),
      );

  Future<http.Response> delete(String url) => _withRefresh(
        () async => http.delete(Uri.parse(url), headers: await _authHeaders(json: false)),
      );

  Future<http.Response> multipart(
    String url, {
    required Map<String, String> fields,
    Map<String, String> files = const {},
    String method = 'POST',
  }) =>
      _withRefresh(() async {
        final request = http.MultipartRequest(method, Uri.parse(url));
        final token = await TokenStorage.instance.getAccessToken();
        if (token != null) request.headers['Authorization'] = 'Bearer $token';
        request.fields.addAll(fields);
        for (final entry in files.entries) {
          request.files.add(await http.MultipartFile.fromPath(entry.key, entry.value));
        }
        final streamed = await request.send();
        return http.Response.fromStream(streamed);
      });

  Future<http.Response> _withRefresh(Future<http.Response> Function() attempt) async {
    final first = await attempt();
    if (first.statusCode != 401) return first;

    final refreshed = await _tryRefresh();
    if (!refreshed) {
      onSessionExpired?.call();
      throw SessionExpiredException();
    }
    return attempt();
  }

  Future<bool> _tryRefresh() async {
    final refreshToken = await TokenStorage.instance.getRefreshToken();
    if (refreshToken == null) return false;
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.loginRefresh),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh': refreshToken}),
      );
      if (response.statusCode != 200) return false;
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final newAccess = data['access'] as String?;
      if (newAccess == null) return false;
      await TokenStorage.instance.saveAccessToken(newAccess);
      return true;
    } on SocketException {
      return false;
    }
  }
}
