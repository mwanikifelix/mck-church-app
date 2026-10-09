import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/event_model.dart';

class EventsService {
  Future<List<EventModel>> fetchEvents() async {
    final response = await ApiClient.instance.get(ApiConfig.events);
    if (response.statusCode != 200) {
      throw Exception('Failed to load events (${response.statusCode})');
    }
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => EventModel.fromJson(e)).toList();
  }

  Future<void> rsvp(String eventId, String status) async {
    final response = await ApiClient.instance.post(
      '${ApiConfig.events}$eventId/rsvp/',
      body: {'status': status},
    );
    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to RSVP (${response.statusCode})');
    }
  }
}
