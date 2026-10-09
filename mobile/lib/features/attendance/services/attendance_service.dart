import 'dart:convert';
import 'package:geolocator/geolocator.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/attendance_record_model.dart';

class CheckInResult {
  final bool success;
  final String message;
  CheckInResult(this.success, this.message);
}

class AttendanceService {
  Future<List<AttendanceRecordModel>> fetchHistory() async {
    final response = await ApiClient.instance.get(ApiConfig.attendanceMine);
    if (response.statusCode != 200) throw Exception('attendance ${response.statusCode}');
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => AttendanceRecordModel.fromJson(e)).toList();
  }

  /// Gets the phone's position, then asks the server to verify the
  /// member is inside the branch radius. The distance check happens
  /// server-side so it can't be bypassed by editing the app.
  Future<CheckInResult> checkIn() async {
    final serviceOn = await Geolocator.isLocationServiceEnabled();
    if (!serviceOn) {
      return CheckInResult(false, 'Turn on your phone location (GPS) and try again.');
    }

    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
      return CheckInResult(false, 'Location permission is needed to check in. Enable it in app settings.');
    }

    final position = await Geolocator.getCurrentPosition(
      locationSettings: const LocationSettings(accuracy: LocationAccuracy.high),
    );

    final response = await ApiClient.instance.post(
      ApiConfig.attendanceCheckIn,
      body: {'latitude': position.latitude, 'longitude': position.longitude},
    );

    if (response.statusCode == 201) return CheckInResult(true, 'You are checked in. God bless you!');
    if (response.statusCode == 200) return CheckInResult(true, 'You already checked in today.');

    try {
      final data = jsonDecode(response.body);
      if (data is Map && data['detail'] != null) return CheckInResult(false, data['detail'].toString());
    } catch (_) {}
    return CheckInResult(false, 'Check-in failed. Please try again.');
  }
}
