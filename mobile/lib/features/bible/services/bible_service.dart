import 'dart:convert';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_config.dart';
import '../models/bible_verse_model.dart';
import '../models/bible_version_model.dart';
import '../models/hymn_model.dart';

class BibleService {
  Future<List<BibleVersionModel>> fetchVersions() async {
    final response = await ApiClient.instance.get(ApiConfig.bibleVersions);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => BibleVersionModel.fromJson(e)).toList();
  }

  Future<List<BibleVerseModel>> fetchReading({
    required String versionCode,
    required String book,
    required int chapter,
  }) async {
    final url = '${ApiConfig.bibleVerseReference}?version=$versionCode&book=$book&chapter=$chapter';
    final response = await ApiClient.instance.get(url);
    if (response.statusCode != 200) return [];
    return (jsonDecode(response.body) as List).map((e) => BibleVerseModel.fromJson(e)).toList();
  }

  Future<List<HymnModel>> fetchHymns() async {
    final response = await ApiClient.instance.get(ApiConfig.hymns);
    if (response.statusCode != 200) return [];
    final data = jsonDecode(response.body);
    final list = data is Map ? (data['results'] ?? []) : data;
    return (list as List).map((e) => HymnModel.fromJson(e)).toList();
  }
}
