import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/section_header.dart';
import '../../../widgets/soft_card.dart';
import '../../../widgets/state_views.dart';
import '../models/attendance_record_model.dart';
import '../services/attendance_service.dart';

class AttendanceScreen extends StatefulWidget {
  const AttendanceScreen({super.key});

  @override
  State<AttendanceScreen> createState() => _AttendanceScreenState();
}

class _AttendanceScreenState extends State<AttendanceScreen> {
  final _service = AttendanceService();
  late Future<List<AttendanceRecordModel>> _history;
  bool _checkingIn = false;
  CheckInResult? _lastResult;

  @override
  void initState() {
    super.initState();
    _history = _service.fetchHistory();
  }

  Future<void> _refresh() async {
    setState(() => _history = _service.fetchHistory());
    await _history;
  }

  Future<void> _checkIn() async {
    setState(() {
      _checkingIn = true;
      _lastResult = null;
    });
    CheckInResult result;
    try {
      result = await _service.checkIn();
    } catch (_) {
      result = CheckInResult(false, 'Could not get your location. Please try again.');
    }
    if (!mounted) return;
    setState(() {
      _checkingIn = false;
      _lastResult = result;
    });
    if (result.success) _refresh();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sunday Attendance')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: AppColors.primary,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            SoftCard(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  Container(
                    width: 84,
                    height: 84,
                    decoration: const BoxDecoration(color: AppColors.primarySoft, shape: BoxShape.circle),
                    child: const Icon(Icons.location_on, color: AppColors.primary, size: 40),
                  ),
                  const SizedBox(height: 16),
                  Text('Check in at church', style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 6),
                  Text(
                    'You must be at your branch to check in. Your location is only used to confirm you are on site.',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton.icon(
                    onPressed: _checkingIn ? null : _checkIn,
                    icon: _checkingIn
                        ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                        : const Icon(Icons.check_circle_outline),
                    label: Text(_checkingIn ? 'Checking location...' : 'Check In Now'),
                  ),
                  if (_lastResult != null) ...[
                    const SizedBox(height: 16),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: _lastResult!.success ? AppColors.successSoft : AppColors.dangerSoft,
                        borderRadius: BorderRadius.circular(AppRadius.sm),
                      ),
                      child: Text(
                        _lastResult!.message,
                        style: TextStyle(
                          color: _lastResult!.success ? AppColors.success : AppColors.danger,
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 24),
            const SectionHeader(title: 'My Attendance'),
            const SizedBox(height: 12),
            FutureBuilder<List<AttendanceRecordModel>>(
              future: _history,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Padding(padding: EdgeInsets.symmetric(vertical: 30), child: LoadingView());
                }
                if (snapshot.hasError) {
                  return ErrorView(message: 'Could not load your attendance.', onRetry: _refresh);
                }
                final records = snapshot.data!;
                if (records.isEmpty) {
                  return const SoftCard(
                    child: EmptyView(message: 'No check-ins yet.', icon: Icons.event_available_outlined),
                  );
                }
                return Column(
                  children: records
                      .map((r) => Padding(
                            padding: const EdgeInsets.only(bottom: 10),
                            child: SoftCard(
                              child: Row(
                                children: [
                                  Container(
                                    width: 40,
                                    height: 40,
                                    decoration: BoxDecoration(color: AppColors.successSoft, borderRadius: BorderRadius.circular(AppRadius.sm)),
                                    child: const Icon(Icons.check, color: AppColors.success, size: 20),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(r.branchName, style: Theme.of(context).textTheme.titleMedium),
                                        Text(
                                          DateFormat('EEE d MMM yyyy, h:mm a').format(r.checkedInAt),
                                          style: Theme.of(context).textTheme.bodyMedium,
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ))
                      .toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
