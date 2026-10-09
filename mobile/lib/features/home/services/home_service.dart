import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../../events_feed/models/event_model.dart';
import '../models/clergy_model.dart';
import '../models/livestream_model.dart';

class HomeData {
  final List<EventModel> upcomingEvents;
  final List<ClergyModel> leadership;
  final LivestreamModel? liveNow;

  HomeData({required this.upcomingEvents, required this.leadership, this.liveNow});
}

class HomeService {
  Future<HomeData> loadHome() async {
    final results = await Future.wait([
      _fetchEvents(),
      _fetchClergy(),
      _fetchLivestreams(),
    ]);

    final events = results[0] as List<EventModel>;
    final clergy = results[1] as List<ClergyModel>;
    final livestreams = results[2] as List<LivestreamModel>;

    final now = DateTime.now();
    final upcoming = events.where((e) => e.startTime.isAfter(now)).toList()
      ..sort((a, b) => a.startTime.compareTo(b.startTime));

    LivestreamModel? live;
    for (final ls in livestreams) {
      if (ls.isLive) {
        live = ls;
        break;
      }
    }

    return HomeData(
      upcomingEvents: upcoming.take(5).toList(),
      leadership: clergy.take(8).toList(),
      liveNow: live,
    );
  }

  Future<List<EventModel>> _fetchEvents() async {
    final response = await ApiClient.instance.get(ApiConfig.events);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => EventModel.fromJson(e)).toList();
  }

  Future<List<ClergyModel>> _fetchClergy() async {
    final response = await ApiClient.instance.get(ApiConfig.clergy);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => ClergyModel.fromJson(e)).toList();
  }

  Future<List<LivestreamModel>> _fetchLivestreams() async {
    final response = await ApiClient.instance.get(ApiConfig.livestreams);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => LivestreamModel.fromJson(e)).toList();
  }
}
