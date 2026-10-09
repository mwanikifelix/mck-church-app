import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/section_header.dart';
import '../../../widgets/soft_card.dart';
import '../../../widgets/state_views.dart';
import '../models/catechism_models.dart';
import '../services/catechism_service.dart';

class _CatechismData {
  final List<RegistrationWindowModel> windows;
  final List<CatechismRegistrationModel> mine;
  _CatechismData(this.windows, this.mine);
}

class CatechismScreen extends StatefulWidget {
  const CatechismScreen({super.key});

  @override
  State<CatechismScreen> createState() => _CatechismScreenState();
}

class _CatechismScreenState extends State<CatechismScreen> {
  final _service = CatechismService();
  late Future<_CatechismData> _future;
  String? _registeringId;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<_CatechismData> _load() async {
    final results = await Future.wait([_service.fetchWindows(), _service.fetchMyRegistrations()]);
    return _CatechismData(
      results[0] as List<RegistrationWindowModel>,
      results[1] as List<CatechismRegistrationModel>,
    );
  }

  Future<void> _refresh() async {
    setState(() => _future = _load());
    await _future;
  }

  Future<void> _register(RegistrationWindowModel window) async {
    setState(() => _registeringId = window.id);
    final error = await _service.register(window.id);
    if (!mounted) return;
    setState(() => _registeringId = null);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(error ?? 'Registered for ${window.name}'),
        backgroundColor: error == null ? null : AppColors.danger,
      ),
    );
    if (error == null) _refresh();
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'confirmed':
        return AppColors.info;
      case 'completed':
        return AppColors.success;
      default:
        return AppColors.warning;
    }
  }

  @override
  Widget build(BuildContext context) {
    final fmt = DateFormat('d MMM yyyy, h:mm a');
    return Scaffold(
      appBar: AppBar(title: const Text('Catechism')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: AppColors.primary,
        child: FutureBuilder<_CatechismData>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
            if (snapshot.hasError) {
              return ErrorView(message: 'Could not load catechism registration.', onRetry: _refresh);
            }
            final data = snapshot.data!;
            final registeredWindowIds = data.mine.map((r) => r.windowId).toSet();

            return ListView(
              padding: const EdgeInsets.all(20),
              children: [
                const SectionHeader(title: 'Registration Periods'),
                const SizedBox(height: 12),
                if (data.windows.isEmpty)
                  const SoftCard(
                    child: EmptyView(
                      message: 'No registration period has been announced yet.',
                      icon: Icons.event_busy_outlined,
                    ),
                  )
                else
                  ...data.windows.map((w) {
                    final alreadyIn = registeredWindowIds.contains(w.id);
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: SoftCard(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Expanded(child: Text(w.name, style: Theme.of(context).textTheme.titleMedium)),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                                  decoration: BoxDecoration(
                                    color: w.isOpen ? AppColors.successSoft : AppColors.border,
                                    borderRadius: BorderRadius.circular(AppRadius.pill),
                                  ),
                                  child: Text(
                                    w.isOpen ? 'OPEN' : 'CLOSED',
                                    style: TextStyle(
                                      fontSize: 10,
                                      fontWeight: FontWeight.w800,
                                      color: w.isOpen ? AppColors.success : AppColors.textSecondary,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            if (w.description.isNotEmpty) ...[
                              const SizedBox(height: 4),
                              Text(w.description, style: Theme.of(context).textTheme.bodyMedium),
                            ],
                            const SizedBox(height: 8),
                            Text('Opens: ${fmt.format(w.opensAt)}', style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                            Text('Closes: ${fmt.format(w.closesAt)}', style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                            const SizedBox(height: 12),
                            SizedBox(
                              width: double.infinity,
                              child: ElevatedButton(
                                onPressed: (!w.isOpen || alreadyIn || _registeringId == w.id) ? null : () => _register(w),
                                child: _registeringId == w.id
                                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                                    : Text(alreadyIn ? 'Already Registered' : (w.isOpen ? 'Register' : 'Registration Closed')),
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                const SizedBox(height: 12),
                const SectionHeader(title: 'My Registrations'),
                const SizedBox(height: 12),
                if (data.mine.isEmpty)
                  const SoftCard(child: EmptyView(message: 'You have not registered yet.', icon: Icons.school_outlined))
                else
                  ...data.mine.map((r) => Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: SoftCard(
                          child: Row(
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(r.windowName, style: Theme.of(context).textTheme.titleMedium),
                                    Text(DateFormat('d MMM yyyy').format(r.submittedAt), style: Theme.of(context).textTheme.bodyMedium),
                                  ],
                                ),
                              ),
                              Text(r.status.toUpperCase(), style: TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: _statusColor(r.status))),
                            ],
                          ),
                        ),
                      )),
              ],
            );
          },
        ),
      ),
    );
  }
}
