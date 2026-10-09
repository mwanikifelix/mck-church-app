import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../../../widgets/soft_card.dart';
import '../models/event_model.dart';
import '../services/events_service.dart';

class EventsScreen extends StatefulWidget {
  const EventsScreen({super.key});

  @override
  State<EventsScreen> createState() => _EventsScreenState();
}

class _EventsScreenState extends State<EventsScreen> {
  final _service = EventsService();
  late Future<List<EventModel>> _eventsFuture;

  @override
  void initState() {
    super.initState();
    _eventsFuture = _service.fetchEvents();
  }

  Future<void> _refresh() async {
    setState(() => _eventsFuture = _service.fetchEvents());
    await _eventsFuture;
  }

  Future<void> _showRsvpSheet(EventModel event) async {
    final choice = await showModalBottomSheet<String>(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(AppRadius.lg))),
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 12),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                child: Text('RSVP to "${event.title}"', style: Theme.of(context).textTheme.titleMedium),
              ),
              ListTile(leading: const Icon(Icons.check_circle_outline, color: AppColors.success), title: const Text('Attending'), onTap: () => Navigator.pop(ctx, 'attending')),
              ListTile(leading: const Icon(Icons.help_outline, color: AppColors.warning), title: const Text('Maybe'), onTap: () => Navigator.pop(ctx, 'maybe')),
              ListTile(leading: const Icon(Icons.cancel_outlined, color: AppColors.danger), title: const Text('Not Attending'), onTap: () => Navigator.pop(ctx, 'not_attending')),
            ],
          ),
        ),
      ),
    );
    if (choice == null || !mounted) return;
    try {
      await _service.rsvp(event.id, choice);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('RSVP saved')));
        _refresh();
      }
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Could not save RSVP'), backgroundColor: AppColors.danger));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Events')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: AppColors.primary,
        child: FutureBuilder<List<EventModel>>(
          future: _eventsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
            if (snapshot.hasError) return ErrorView(message: 'Could not load events.', onRetry: _refresh);
            final events = snapshot.data!..sort((a, b) => a.startTime.compareTo(b.startTime));
            if (events.isEmpty) {
              return const EmptyView(message: 'No events scheduled right now.', icon: Icons.event_busy_outlined);
            }
            return ListView.separated(
              padding: const EdgeInsets.all(20),
              itemCount: events.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final event = events[index];
                return SoftCard(
                  onTap: () => _showRsvpSheet(event),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        width: 52, height: 52,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(color: AppColors.primarySoft, borderRadius: BorderRadius.circular(AppRadius.sm)),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(DateFormat('MMM').format(event.startTime).toUpperCase(), style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w800, color: AppColors.primary)),
                            Text(DateFormat('d').format(event.startTime), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.primary)),
                          ],
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(event.title, style: Theme.of(context).textTheme.titleMedium),
                            const SizedBox(height: 4),
                            Text(DateFormat('h:mm a').format(event.startTime), style: Theme.of(context).textTheme.bodyMedium),
                            if (event.location.isNotEmpty) ...[
                              const SizedBox(height: 2),
                              Row(children: [
                                const Icon(Icons.place_outlined, size: 13, color: AppColors.textMuted),
                                const SizedBox(width: 4),
                                Expanded(child: Text(event.location, style: const TextStyle(fontSize: 12, color: AppColors.textMuted), maxLines: 1, overflow: TextOverflow.ellipsis)),
                              ]),
                            ],
                            const SizedBox(height: 6),
                            Row(children: [
                              const Icon(Icons.people_outline, size: 13, color: AppColors.textMuted),
                              const SizedBox(width: 4),
                              Text('${event.rsvpCount} attending', style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                            ]),
                          ],
                        ),
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
