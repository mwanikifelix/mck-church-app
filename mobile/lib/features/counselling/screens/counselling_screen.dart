import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/soft_card.dart';
import '../../../widgets/state_views.dart';
import '../models/counselling_request_model.dart';
import '../services/counselling_service.dart';

class CounsellingScreen extends StatefulWidget {
  const CounsellingScreen({super.key});

  @override
  State<CounsellingScreen> createState() => _CounsellingScreenState();
}

class _CounsellingScreenState extends State<CounsellingScreen> {
  final _service = CounsellingService();
  late Future<List<CounsellingRequestModel>> _future;

  @override
  void initState() {
    super.initState();
    _future = _service.fetchMine();
  }

  Future<void> _refresh() async {
    setState(() => _future = _service.fetchMine());
    await _future;
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'confirmed':
        return AppColors.info;
      case 'completed':
        return AppColors.success;
      case 'cancelled':
        return AppColors.danger;
      default:
        return AppColors.warning;
    }
  }

  Future<void> _cancel(CounsellingRequestModel r) async {
    final ok = await _service.cancel(r.id);
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(ok ? 'Request cancelled' : 'Could not cancel this request'),
        backgroundColor: ok ? null : AppColors.danger,
      ),
    );
    if (ok) _refresh();
  }

  Future<void> _openRequestSheet() async {
    final controller = TextEditingController();
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
                  Text('Request Counselling', style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 4),
                  Text(
                    'Share briefly what you need. A counsellor will confirm a date and time with you. This is private.',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
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
                    decoration: const InputDecoration(hintText: 'What would you like to talk about?'),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: submitting
                        ? null
                        : () async {
                            if (controller.text.trim().isEmpty) return;
                            setSheetState(() {
                              submitting = true;
                              error = null;
                            });
                            final ok = await _service.submit(controller.text.trim());
                            if (ok) {
                              if (ctx.mounted) Navigator.pop(ctx);
                              _refresh();
                            } else {
                              setSheetState(() {
                                submitting = false;
                                error = 'Could not send your request. Please try again.';
                              });
                            }
                          },
                    child: submitting
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                        : const Text('Send Request'),
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
      appBar: AppBar(title: const Text('Counselling')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _openRequestSheet,
        icon: const Icon(Icons.add),
        label: const Text('New Request'),
      ),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: AppColors.primary,
        child: FutureBuilder<List<CounsellingRequestModel>>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
            if (snapshot.hasError) return ErrorView(message: 'Could not load your requests.', onRetry: _refresh);
            final requests = snapshot.data!;
            if (requests.isEmpty) {
              return const EmptyView(
                message: 'No counselling requests yet. Tap "New Request" to ask for guidance.',
                icon: Icons.support_agent_outlined,
              );
            }
            return ListView.separated(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 90),
              itemCount: requests.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final r = requests[index];
                return SoftCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Text(
                            DateFormat('d MMM yyyy').format(r.requestedAt),
                            style: const TextStyle(fontSize: 12, color: AppColors.textMuted),
                          ),
                          const Spacer(),
                          Text(
                            r.status.toUpperCase(),
                            style: TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: _statusColor(r.status)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text(r.message, style: Theme.of(context).textTheme.bodyLarge),
                      if (r.confirmedDatetime != null) ...[
                        const SizedBox(height: 10),
                        Row(
                          children: [
                            const Icon(Icons.event_available, size: 16, color: AppColors.info),
                            const SizedBox(width: 6),
                            Expanded(
                              child: Text(
                                'Scheduled: ${DateFormat('EEE d MMM, h:mm a').format(r.confirmedDatetime!)}'
                                '${r.counsellorName != null ? ' with ${r.counsellorName}' : ''}',
                                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                              ),
                            ),
                          ],
                        ),
                      ],
                      if (r.status == 'pending' || r.status == 'confirmed') ...[
                        const SizedBox(height: 8),
                        Align(
                          alignment: Alignment.centerRight,
                          child: TextButton(
                            onPressed: () => _cancel(r),
                            child: const Text('Cancel request', style: TextStyle(color: AppColors.danger)),
                          ),
                        ),
                      ],
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
