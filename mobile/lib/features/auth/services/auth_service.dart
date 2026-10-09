import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../../../core/api/token_storage.dart';
import '../../../core/models/user_model.dart';

class AuthResult {
  final bool success;
  final UserModel? user;
  final String? generalError;
  final Map<String, String> fieldErrors;

  AuthResult.ok(this.user)
      : success = true,
        generalError = null,
        fieldErrors = const {};

  AuthResult.error({this.generalError, this.fieldErrors = const {}})
      : success = false,
        user = null;
}

class AuthService extends ChangeNotifier {
  AuthService._internal() {
    ApiClient.instance.onSessionExpired = _forceLogoutLocal;
  }
  static final AuthService instance = AuthService._internal();

  UserModel? _currentUser;
  bool _isLoading = false;

  UserModel? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _currentUser != null;

  Future<bool> tryAutoLogin() async {
    final refresh = await TokenStorage.instance.getRefreshToken();
    if (refresh == null) return false;
    try {
      await _fetchMe();
      return _currentUser != null;
    } catch (_) {
      await _forceLogoutLocal();
      return false;
    }
  }

  Future<AuthResult> login({required String email, required String password}) async {
    _isLoading = true;
    notifyListeners();
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.login),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        await TokenStorage.instance.saveTokens(
          access: data['access'] as String,
          refresh: data['refresh'] as String,
        );
        await _fetchMe();
        _isLoading = false;
        notifyListeners();
        return AuthResult.ok(_currentUser);
      }

      return _handleErrorResponse(response);
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      return AuthResult.error(generalError: 'Could not reach the server. Check your connection and try again.');
    }
  }

  Future<AuthResult> register({
    required String fullName,
    required String email,
    required String password,
    required String confirmPassword,
    String? branchId,
    File? photo,
  }) async {
    final fieldErrors = <String, String>{};
    if (fullName.trim().isEmpty) fieldErrors['full_name'] = 'Full name is required';
    if (email.trim().isEmpty) {
      fieldErrors['email'] = 'Email is required';
    } else if (!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(email.trim())) {
      fieldErrors['email'] = 'Enter a valid email address';
    }
    if (password.isEmpty) {
      fieldErrors['password'] = 'Password is required';
    } else if (password.length < 8) {
      fieldErrors['password'] = 'Minimum 8 characters';
    }
    if (confirmPassword != password) {
      fieldErrors['confirm_password'] = 'Passwords do not match';
    }
    if (fieldErrors.isNotEmpty) {
      return AuthResult.error(fieldErrors: fieldErrors);
    }

    _isLoading = true;
    notifyListeners();
    try {
      final response = await ApiClient.instance.multipart(
        ApiConfig.signup,
        fields: {
          'full_name': fullName.trim(),
          'email': email.trim(),
          'password': password,
          'confirm_password': confirmPassword,
          if (branchId != null) 'branch': branchId,
        },
        files: photo != null ? {'passport_photo': photo.path} : {},
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        final tokens = data['tokens'] as Map<String, dynamic>;
        await TokenStorage.instance.saveTokens(
          access: tokens['access'] as String,
          refresh: tokens['refresh'] as String,
        );
        _currentUser = UserModel.fromJson(data['user'] as Map<String, dynamic>);
        _isLoading = false;
        notifyListeners();
        return AuthResult.ok(_currentUser);
      }

      return _handleErrorResponse(response);
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      return AuthResult.error(generalError: 'Could not reach the server. Check your connection and try again.');
    }
  }

  Future<AuthResult> loginWithGoogle(String idToken) async {
    _isLoading = true;
    notifyListeners();
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.googleLogin),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'id_token': idToken}),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        final tokens = data['tokens'] as Map<String, dynamic>;
        await TokenStorage.instance.saveTokens(
          access: tokens['access'] as String,
          refresh: tokens['refresh'] as String,
        );
        _currentUser = UserModel.fromJson(data['user'] as Map<String, dynamic>);
        _isLoading = false;
        notifyListeners();
        return AuthResult.ok(_currentUser);
      }
      return _handleErrorResponse(response);
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      return AuthResult.error(generalError: 'Google sign-in failed. Please try again.');
    }
  }

  Future<void> refreshProfile() => _fetchMe();

  Future<void> _fetchMe() async {
    final response = await ApiClient.instance.get(ApiConfig.me);
    if (response.statusCode == 200) {
      _currentUser = UserModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
      notifyListeners();
    } else {
      throw Exception('Failed to load profile (${response.statusCode})');
    }
  }

  Future<void> logout() async {
    await _forceLogoutLocal();
  }

  Future<void> _forceLogoutLocal() async {
    await TokenStorage.instance.clear();
    _currentUser = null;
    notifyListeners();
  }

  AuthResult _handleErrorResponse(http.Response response) {
    _isLoading = false;
    notifyListeners();
    try {
      final data = jsonDecode(response.body);
      if (data is Map<String, dynamic>) {
        final fieldErrors = <String, String>{};
        String? general;
        data.forEach((key, value) {
          final message = value is List ? value.join(', ') : value.toString();
          if (key == 'detail' || key == 'non_field_errors') {
            general = message;
          } else {
            fieldErrors[key] = message;
          }
        });
        return AuthResult.error(generalError: general, fieldErrors: fieldErrors);
      }
    } catch (_) {
      // fall through
    }
    return AuthResult.error(generalError: 'Something went wrong (${response.statusCode}). Please try again.');
  }
}
