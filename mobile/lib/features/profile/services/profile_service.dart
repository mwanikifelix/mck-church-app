import 'dart:convert';
import 'dart:typed_data';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/membership_card_model.dart';

class ProfileService {
  Future<MembershipCardModel> fetchMyCard() async {
    final response = await ApiClient.instance.get(ApiConfig.membershipCard);
    if (response.statusCode != 200) {
      throw Exception('Failed to load membership card (${response.statusCode})');
    }
    return MembershipCardModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  /// The QR endpoint returns a raw PNG, not JSON — needs the auth
  /// header attached the same way, so it goes through ApiClient too,
  /// just read as bytes instead of decoded as JSON.
  Future<Uint8List> fetchMyQrCode() async {
    final response = await ApiClient.instance.get(ApiConfig.meQr);
    if (response.statusCode != 200) {
      throw Exception('Failed to load QR code (${response.statusCode})');
    }
    return response.bodyBytes;
  }
}
