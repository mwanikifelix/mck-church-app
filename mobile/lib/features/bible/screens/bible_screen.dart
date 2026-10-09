import 'package:flutter/material.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../../../widgets/soft_card.dart';
import '../models/bible_verse_model.dart';
import '../models/bible_version_model.dart';
import '../models/hymn_model.dart';
import '../services/bible_service.dart';

class BibleScreen extends StatefulWidget {
  const BibleScreen({super.key});

  @override
  State<BibleScreen> createState() => _BibleScreenState();
}

class _BibleScreenState extends State<BibleScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bible & Hymns'),
        bottom: TabBar(
          controller: _tabController,
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textMuted,
          indicatorColor: AppColors.primary,
          tabs: const [Tab(text: 'Read'), Tab(text: 'Hymns')],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: const [_BibleReadTab(), _HymnsTab()],
      ),
    );
  }
}

class _BibleReadTab extends StatefulWidget {
  const _BibleReadTab();

  @override
  State<_BibleReadTab> createState() => _BibleReadTabState();
}

class _BibleReadTabState extends State<_BibleReadTab> {
  final _service = BibleService();
  final _bookController = TextEditingController(text: 'John');
  final _chapterController = TextEditingController(text: '3');

  List<BibleVersionModel> _versions = [];
  BibleVersionModel? _selectedVersion;
  List<BibleVerseModel> _verses = [];
  bool _loadingVersions = true;
  bool _loadingReading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadVersions();
  }

  @override
  void dispose() {
    _bookController.dispose();
    _chapterController.dispose();
    super.dispose();
  }

  Future<void> _loadVersions() async {
    final versions = await _service.fetchVersions();
    setState(() {
      _versions = versions;
      _selectedVersion = versions.isNotEmpty ? versions.first : null;
      _loadingVersions = false;
    });
    if (_selectedVersion != null) _loadReading();
  }

  Future<void> _loadReading() async {
    if (_selectedVersion == null || _bookController.text.trim().isEmpty) return;
    final chapter = int.tryParse(_chapterController.text.trim()) ?? 1;
    setState(() {
      _loadingReading = true;
      _error = null;
    });
    try {
      final verses = await _service.fetchReading(
        versionCode: _selectedVersion!.code,
        book: _bookController.text.trim(),
        chapter: chapter,
      );
      setState(() {
        _verses = verses;
        _loadingReading = false;
        if (verses.isEmpty) _error = 'No verses found for this reference in ${_selectedVersion!.code}.';
      });
    } catch (_) {
      setState(() {
        _loadingReading = false;
        _error = 'Could not load this passage.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loadingVersions) return const LoadingView();
    if (_versions.isEmpty) {
      return const EmptyView(
        message: 'No Bible versions have been added yet. Check back soon.',
        icon: Icons.menu_book_outlined,
      );
    }

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: TextField(
                      controller: _bookController,
                      decoration: const InputDecoration(labelText: 'Book', isDense: true),
                      onSubmitted: (_) => _loadReading(),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextField(
                      controller: _chapterController,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'Ch.', isDense: true),
                      onSubmitted: (_) => _loadReading(),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: DropdownButtonFormField<BibleVersionModel>(
                      value: _selectedVersion,
                      isExpanded: true,
                      decoration: const InputDecoration(labelText: 'Version', isDense: true),
                      items: _versions
                          .map((v) => DropdownMenuItem(value: v, child: Text('${v.code} — ${v.language}')))
                          .toList(),
                      onChanged: (v) {
                        setState(() => _selectedVersion = v);
                        _loadReading();
                      },
                    ),
                  ),
                  const SizedBox(width: 10),
                  ElevatedButton(onPressed: _loadReading, child: const Text('Go')),
                ],
              ),
            ],
          ),
        ),
        Expanded(
          child: _loadingReading
              ? const LoadingView()
              : _error != null
                  ? EmptyView(message: _error!, icon: Icons.menu_book_outlined)
                  : ListView.builder(
                      padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
                      itemCount: _verses.length,
                      itemBuilder: (context, index) {
                        final v = _verses[index];
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: RichText(
                            text: TextSpan(
                              children: [
                                TextSpan(text: '${v.verseNumber}  ', style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.w800, fontSize: 13)),
                                TextSpan(text: v.text, style: const TextStyle(color: AppColors.textPrimary, fontSize: 15, height: 1.5)),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
        ),
      ],
    );
  }
}

class _HymnsTab extends StatefulWidget {
  const _HymnsTab();

  @override
  State<_HymnsTab> createState() => _HymnsTabState();
}

class _HymnsTabState extends State<_HymnsTab> {
  final _service = BibleService();
  final _searchController = TextEditingController();
  List<HymnModel> _allHymns = [];
  List<HymnModel> _filtered = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
    _searchController.addListener(_filter);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    final hymns = await _service.fetchHymns();
    setState(() {
      _allHymns = hymns;
      _filtered = hymns;
      _loading = false;
    });
  }

  void _filter() {
    final query = _searchController.text.trim().toLowerCase();
    setState(() {
      _filtered = query.isEmpty
          ? _allHymns
          : _allHymns.where((h) {
              return h.number.toString() == query ||
                  h.title.toLowerCase().contains(query) ||
                  h.firstLine.toLowerCase().contains(query);
            }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const LoadingView();

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16),
          child: TextField(
            controller: _searchController,
            decoration: const InputDecoration(
              hintText: 'Search by number or first line...',
              prefixIcon: Icon(Icons.search),
              isDense: true,
            ),
          ),
        ),
        Expanded(
          child: _filtered.isEmpty
              ? const EmptyView(message: 'No hymns match your search.', icon: Icons.search_off)
              : ListView.separated(
                  padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                  itemCount: _filtered.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 8),
                  itemBuilder: (context, index) {
                    final hymn = _filtered[index];
                    return SoftCard(
                      onTap: () {},
                      child: Row(
                        children: [
                          Container(
                            width: 40, height: 40,
                            alignment: Alignment.center,
                            decoration: BoxDecoration(color: AppColors.primarySoft, borderRadius: BorderRadius.circular(AppRadius.sm)),
                            child: Text('${hymn.number}', style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.w800, fontSize: 12)),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(hymn.title, style: Theme.of(context).textTheme.titleMedium),
                                if (hymn.firstLine.isNotEmpty)
                                  Text(hymn.firstLine, style: Theme.of(context).textTheme.bodyMedium, maxLines: 1, overflow: TextOverflow.ellipsis),
                              ],
                            ),
                          ),
                          if (hymn.fileType != null)
                            Icon(
                              hymn.fileType == 'pdf' ? Icons.picture_as_pdf_outlined
                                  : hymn.fileType == 'image' ? Icons.image_outlined
                                  : hymn.fileType == 'ppt' ? Icons.slideshow_outlined
                                  : Icons.text_snippet_outlined,
                              color: AppColors.textMuted,
                              size: 18,
                            ),
                        ],
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }
}
