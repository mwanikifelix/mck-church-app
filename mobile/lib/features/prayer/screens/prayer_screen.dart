import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../../../widgets/soft_card.dart';
import '../models/prayer_request_model.dart';
import '../services/prayer_service.dart';

class PrayerScreen extends StatefulWidget {
  const PrayerScreen({super.key});

  @override
  State<PrayerScreen> createState() => _PrayerScreenState();
}

class _PrayerScreenState extends State<PrayerScreen> {
  final _service = PrayerService();
  late Future<List<PrayerRequestModel>> _future;
  final Set<String> _supported = {};

  @override
  void initState() {
    super.initState();
    _future = _service.fetchRequests();
  }

  Future<void> _refresh() async {
    setState(() => _future = _service.fetchRequests());
    await _future;
  }

  Future<void> _support(PrayerRequestModel request) async {
    final ok = await _service.markSupporting(request.id);
    if (ok && mounted) {
      setState(() => _supported.add(request.id));
      _refresh();
    }
  }

  Future<void> _openSubmitSheet() async {
    final controller = TextEditingController();
    bool isAnonymous = false;
    bool submitting = false;
    String? error;

    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(AppRadius.lg))),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (ctx, setSheetState) {
            return Padding(
              padding: EdgeInsets.only(left: 20, right: 20, top: 20, bottom: MediaQuery.of(ctx).viewInsets.bottom + 20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text('Submit a Prayer Request', style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 4),
                  Text('Only you and the pastoral team can see this.', style: Theme.of(context).textTheme.bodyMedium),
                  const SizedBox(height: 16),
                  if (error != null) ...[
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(color: AppColors.dangerSoft, borderRadius: BorderRadius.circular(AppRadius.sm)),
                      child: Text(error!, style: const TextStyle(color: AppColors.danger, fontSize: 12)),
                    ),
                    const SizedBox(height: 12),
                  ],
                  TextField(
                    controller: controller,
                    maxLines: 5,
                    decoration: const InputDecoration(hintText: 'Share what you would like prayer for...'),
                  ),
                  const SizedBox(height: 8),
                  CheckboxListTile(
                    value: isAnonymous,
                    onChanged: (v) => setSheetState(() => isAnonymous = v ?? false),
                    title: const Text('Submit anonymously'),
                    contentPadding: EdgeInsets.zero,
                    controlAffinity: ListTileControlAffinity.leading,
                  ),
                  const SizedBox(height: 12),
                  ElevatedButton(
                    onPressed: submitting
                        ? null
                        : () async {
                            if (controller.text.trim().isEmpty) return;
                            setSheetState(() {
                              submitting = true;
                              error = null;
                            });
                            final ok = await _service.submitRequest(body: controller.text.trim(), isAnonymous: isAnonymous);
                            if (ok) {
                              if (context.mounted) Navigator.pop(ctx);
                              _refresh();
                            } else {
                              setSheetState(() {
                                submitting = false;
                                error = 'Could not submit your request. Please try again.';
                              });
                            }
                          },
                    child: submitting
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                        : const Text('Submit'),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Prayer Requests')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _openSubmitSheet,
        icon: const Icon(Icons.add),
        label: const Text('New Request'),
      ),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: AppColors.primary,
        child: FutureBuilder<List<PrayerRequestModel>>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
            if (snapshot.hasError) return ErrorView(message: 'Could not load prayer requests.', onRetry: _refresh);
            final requests = snapshot.data!;
            if (requests.isEmpty) {
              return const EmptyView(message: 'No prayer requests yet. Tap "New Request" to submit one.', icon: Icons.favorite_border);
            }
            return ListView.separated(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 90),
              itemCount: requests.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final r = requests[index];
                final supported = _supported.contains(r.id);
                return SoftCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              r.isAnonymous ? 'Anonymous' : (r.submitterName ?? 'A member'),
                              style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13),
                            ),
                          ),
                          if (r.status == 'answered')
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                              decoration: BoxDecoration(color: AppColors.successSoft, borderRadius: BorderRadius.circular(AppRadius.pill)),
                              child: const Text('Answered', style: TextStyle(color: AppColors.success, fontSize: 10, fontWeight: FontWeight.w800)),
                            ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text(r.body, style: Theme.of(context).textTheme.bodyLarge),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          Text(DateFormat('d MMM').format(r.createdAt), style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                          const Spacer(),
                          TextButton.icon(
                            onPressed: supported ? null : () => _support(r),
                            icon: Icon(supported ? Icons.favorite : Icons.favorite_border, size: 16, color: supported ? AppColors.danger : AppColors.primary),
                            label: Text('${r.supportCount} praying', style: const TextStyle(fontSize: 12)),
                          ),
                        ],
                      ),
                    ],
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
