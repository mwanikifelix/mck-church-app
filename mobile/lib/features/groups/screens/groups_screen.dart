import 'package:flutter/material.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../../../widgets/soft_card.dart';
import '../models/department_model.dart';
import '../models/growth_group_model.dart';
import '../models/hbc_group_model.dart';
import '../services/groups_service.dart';

class GroupsScreen extends StatefulWidget {
  const GroupsScreen({super.key});

  @override
  State<GroupsScreen> createState() => _GroupsScreenState();
}

class _GroupsScreenState extends State<GroupsScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
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
        title: const Text('Groups'),
        bottom: TabBar(
          controller: _tabController,
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textMuted,
          indicatorColor: AppColors.primary,
          tabs: const [Tab(text: 'My Category'), Tab(text: 'Departments'), Tab(text: 'HBC')],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: const [_GrowthTrackTab(), _DepartmentsTab(), _HbcTab()],
      ),
    );
  }
}

class _GrowthTrackTab extends StatefulWidget {
  const _GrowthTrackTab();
  @override
  State<_GrowthTrackTab> createState() => _GrowthTrackTabState();
}

class _GrowthTrackTabState extends State<_GrowthTrackTab> {
  final _service = GroupsService();
  late Future<List<GrowthGroupModel>> _future;

  @override
  void initState() {
    super.initState();
    _future = _service.fetchGrowthGroups();
  }

  Future<void> _refresh() async {
    setState(() => _future = _service.fetchGrowthGroups());
    await _future;
  }

  Future<void> _join(GrowthGroupModel group) async {
    final error = await _service.joinGrowthGroup(group.id);
    if (!mounted) return;
    if (error == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Joined ${group.name}')));
      _refresh();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error), backgroundColor: AppColors.danger));
    }
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _refresh,
      color: AppColors.primary,
      child: FutureBuilder<List<GrowthGroupModel>>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
          if (snapshot.hasError) return ErrorView(message: 'Could not load groups.', onRetry: _refresh);
          final groups = snapshot.data!;
          if (groups.isEmpty) return const EmptyView(message: 'No growth-track groups available yet.', icon: Icons.group_outlined);
          return ListView.separated(
            padding: const EdgeInsets.all(20),
            itemCount: groups.length,
            separatorBuilder: (_, __) => const SizedBox(height: 12),
            itemBuilder: (context, index) {
              final g = groups[index];
              return SoftCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(g.name, style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 4),
                    if (g.description.isNotEmpty) Text(g.description, style: Theme.of(context).textTheme.bodyMedium),
                    const SizedBox(height: 8),
                    Wrap(spacing: 8, children: [
                      Chip(label: Text('Ages ${g.minAge}-${g.maxAge}')),
                      if (g.maritalStatusRequirement != 'any') Chip(label: Text(g.maritalStatusRequirement)),
                      Chip(label: Text('${g.memberTotal} members')),
                    ]),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton(onPressed: () => _join(g), child: const Text('Join')),
                    ),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class _DepartmentsTab extends StatefulWidget {
  const _DepartmentsTab();
  @override
  State<_DepartmentsTab> createState() => _DepartmentsTabState();
}

class _DepartmentsTabState extends State<_DepartmentsTab> {
  final _service = GroupsService();
  late Future<List<DepartmentModel>> _future;
  final Set<String> _requested = {};

  @override
  void initState() {
    super.initState();
    _future = _service.fetchDepartments();
  }

  Future<void> _refresh() async {
    setState(() => _future = _service.fetchDepartments());
    await _future;
  }

  Future<void> _requestJoin(DepartmentModel dept) async {
    final ok = await _service.requestDepartmentJoin(dept.id);
    if (!mounted) return;
    if (ok) {
      setState(() => _requested.add(dept.id));
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Join request sent for ${dept.name}')));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Could not send join request'), backgroundColor: AppColors.danger));
    }
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _refresh,
      color: AppColors.primary,
      child: FutureBuilder<List<DepartmentModel>>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
          if (snapshot.hasError) return ErrorView(message: 'Could not load departments.', onRetry: _refresh);
          final departments = snapshot.data!;
          if (departments.isEmpty) return const EmptyView(message: 'No departments yet.', icon: Icons.apartment_outlined);
          return ListView.separated(
            padding: const EdgeInsets.all(20),
            itemCount: departments.length,
            separatorBuilder: (_, __) => const SizedBox(height: 12),
            itemBuilder: (context, index) {
              final d = departments[index];
              final requested = _requested.contains(d.id);
              return SoftCard(
                child: Row(
                  children: [
                    Container(
                      width: 44, height: 44,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(color: AppColors.primarySoft, borderRadius: BorderRadius.circular(AppRadius.sm)),
                      child: const Icon(Icons.apartment_outlined, color: AppColors.primary),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(d.name, style: Theme.of(context).textTheme.titleMedium),
                          if (d.meetingDay.isNotEmpty)
                            Text('${d.meetingDay} ${d.meetingTime}', style: Theme.of(context).textTheme.bodyMedium),
                        ],
                      ),
                    ),
                    requested
                        ? const Chip(label: Text('Requested'), backgroundColor: AppColors.warningSoft, labelStyle: TextStyle(color: AppColors.warning))
                        : TextButton(onPressed: () => _requestJoin(d), child: const Text('Join')),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class _HbcTab extends StatefulWidget {
  const _HbcTab();
  @override
  State<_HbcTab> createState() => _HbcTabState();
}

class _HbcTabState extends State<_HbcTab> {
  final _service = GroupsService();
  HbcGroupModel? _myHbc;
  bool _loadingMine = true;
  late Future<List<HbcGroupModel>> _allFuture;

  @override
  void initState() {
    super.initState();
    _allFuture = _service.fetchHbcGroups();
    _loadMyHbc();
  }

  Future<void> _loadMyHbc() async {
    final mine = await _service.fetchMyHbc();
    if (mounted) setState(() {
      _myHbc = mine;
      _loadingMine = false;
    });
  }

  Future<void> _join(HbcGroupModel group) async {
    final ok = await _service.joinHbc(group.id);
    if (!mounted) return;
    if (ok) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Joined ${group.name}')));
      _loadMyHbc();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Could not join this HBC'), backgroundColor: AppColors.danger));
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loadingMine) return const LoadingView();

    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        if (_myHbc != null) ...[
          Text('My HBC Group', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          SoftCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(_myHbc!.name, style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 4),
                Row(children: [const Icon(Icons.place_outlined, size: 14, color: AppColors.textMuted), const SizedBox(width: 4), Text(_myHbc!.location, style: const TextStyle(fontSize: 12, color: AppColors.textMuted))]),
                if (_myHbc!.meetingDay.isNotEmpty) ...[
                  const SizedBox(height: 4),
                  Row(children: [const Icon(Icons.schedule, size: 14, color: AppColors.textMuted), const SizedBox(width: 4), Text('${_myHbc!.meetingDay} ${_myHbc!.meetingTime}', style: const TextStyle(fontSize: 12, color: AppColors.textMuted))]),
                ],
              ],
            ),
          ),
          const SizedBox(height: 24),
        ],
        Text(_myHbc == null ? 'Find an HBC to Join' : 'Other HBC Groups', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 12),
        FutureBuilder<List<HbcGroupModel>>(
          future: _allFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
            if (snapshot.hasError) return const ErrorView(message: 'Could not load HBC groups.');
            final groups = snapshot.data!.where((g) => g.id != _myHbc?.id).toList();
            if (groups.isEmpty) return const EmptyView(message: 'No other HBC groups available.', icon: Icons.groups_outlined);
            return Column(
              children: groups.map((g) => Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: SoftCard(
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(g.name, style: Theme.of(context).textTheme.titleMedium),
                            Text(g.location, style: Theme.of(context).textTheme.bodyMedium),
                          ],
                        ),
                      ),
                      TextButton(onPressed: () => _join(g), child: const Text('Join')),
                    ],
                  ),
                ),
              )).toList(),
            );
          },
        ),
      ],
    );
  }
}
