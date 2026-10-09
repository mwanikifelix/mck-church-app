import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../../../widgets/section_header.dart';
import '../../../widgets/soft_card.dart';
import '../../../widgets/app_bottom_nav.dart';
import '../../auth/services/auth_service.dart';
import '../services/home_service.dart';
import '../models/clergy_model.dart';
import '../../events_feed/models/event_model.dart';
import '../../events_feed/screens/events_screen.dart';
import '../../bible/screens/bible_screen.dart';
import '../../giving/screens/giving_screen.dart';
import '../../profile/screens/profile_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _homeService = HomeService();
  late Future<HomeData> _homeFuture;

  @override
  void initState() {
    super.initState();
    _homeFuture = _homeService.loadHome();
  }

  Future<void> _refresh() async {
    setState(() => _homeFuture = _homeService.loadHome());
    await _homeFuture;
  }

  void _openTab(Widget screen) {
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => screen));
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthService>().currentUser;

    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _refresh,
          color: AppColors.primary,
          child: FutureBuilder<HomeData>(
            future: _homeFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const LoadingView();
              }
              if (snapshot.hasError) {
                return ErrorView(message: 'Could not load home content.', onRetry: _refresh);
              }
              final data = snapshot.data!;
              return ListView(
                padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
                children: [
                  _buildHeader(user?.fullName ?? 'Welcome'),
                  const SizedBox(height: 20),
                  if (data.liveNow != null) ...[
                    _buildLiveBanner(data.liveNow!),
                    const SizedBox(height: 20),
                  ],
                  _buildQuickActions(),
                  const SizedBox(height: 24),
                  SectionHeader(
                    title: 'Upcoming Events',
                    actionLabel: 'View all',
                    onAction: () => _openTab(const EventsScreen()),
                  ),
                  const SizedBox(height: 12),
                  _buildEventsList(data.upcomingEvents),
                  const SizedBox(height: 24),
                  const SectionHeader(title: 'Our Leadership'),
                  const SizedBox(height: 12),
                  _buildLeadershipRow(data.leadership),
                ],
              );
            },
          ),
        ),
      ),
      bottomNavigationBar: AppBottomNav(
        currentIndex: 0,
        onTap: (index) {
          switch (index) {
            case 1:
              _openTab(const EventsScreen());
              break;
            case 2:
              _openTab(const BibleScreen());
              break;
            case 3:
              _openTab(const GivingScreen());
              break;
            case 4:
              _openTab(const ProfileScreen());
              break;
          }
        },
      ),
    );
  }

  Widget _buildHeader(String name) {
    final hour = DateTime.now().hour;
    final greeting = hour < 12 ? 'Good Morning' : (hour < 17 ? 'Good Afternoon' : 'Good Evening');
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(greeting, style: Theme.of(context).textTheme.bodyMedium),
              Text(name, style: Theme.of(context).textTheme.headlineMedium, overflow: TextOverflow.ellipsis),
            ],
          ),
        ),
        IconButton(
          onPressed: () => _openTab(const ProfileScreen()),
          icon: const CircleAvatar(
            backgroundColor: AppColors.primarySoft,
            child: Icon(Icons.person, color: AppColors.primary),
          ),
        ),
      ],
    );
  }

  Widget _buildLiveBanner(dynamic liveNow) {
    return SoftCard(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Container(
            width: 44, height: 44,
            decoration: const BoxDecoration(color: AppColors.dangerSoft, shape: BoxShape.circle),
            child: const Icon(Icons.live_tv, color: AppColors.danger),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(color: AppColors.danger, borderRadius: BorderRadius.circular(AppRadius.pill)),
                      child: const Text('LIVE', style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.w800)),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(liveNow.title, style: Theme.of(context).textTheme.titleMedium, maxLines: 1, overflow: TextOverflow.ellipsis),
              ],
            ),
          ),
          const Icon(Icons.chevron_right, color: AppColors.textMuted),
        ],
      ),
    );
  }

  Widget _buildQuickActions() {
    final actions = [
      (icon: Icons.event_outlined, label: 'Events', onTap: () => _openTab(const EventsScreen())),
      (icon: Icons.menu_book_outlined, label: 'Bible', onTap: () => _openTab(const BibleScreen())),
      (icon: Icons.favorite_outline, label: 'Give', onTap: () => _openTab(const GivingScreen())),
      (icon: Icons.badge_outlined, label: 'My Card', onTap: () => _openTab(const ProfileScreen())),
    ];
    return Row(
      children: actions
          .map((a) => Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  child: _QuickActionButton(icon: a.icon, label: a.label, onTap: a.onTap),
                ),
              ))
          .toList(),
    );
  }

  Widget _buildEventsList(List<EventModel> events) {
    if (events.isEmpty) {
      return const SoftCard(child: EmptyView(message: 'No upcoming events right now.', icon: Icons.event_busy_outlined));
    }
    return SizedBox(
      height: 148,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: events.length,
        separatorBuilder: (_, __) => const SizedBox(width: 12),
        itemBuilder: (context, index) => _EventCard(event: events[index]),
      ),
    );
  }

  Widget _buildLeadershipRow(List<ClergyModel> leadership) {
    if (leadership.isEmpty) {
      return const SoftCard(child: EmptyView(message: 'Leadership directory coming soon.', icon: Icons.groups_outlined));
    }
    return SizedBox(
      height: 110,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: leadership.length,
        separatorBuilder: (_, __) => const SizedBox(width: 16),
        itemBuilder: (context, index) => _LeaderAvatar(clergy: leadership[index]),
      ),
    );
  }
}

class _QuickActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;
  const _QuickActionButton({required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.md),
      child: Column(
        children: [
          Container(
            width: 56, height: 56,
            decoration: BoxDecoration(color: AppColors.primarySoft, borderRadius: BorderRadius.circular(AppRadius.md)),
            child: Icon(icon, color: AppColors.primary),
          ),
          const SizedBox(height: 6),
          Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
        ],
      ),
    );
  }
}

class _EventCard extends StatelessWidget {
  final EventModel event;
  const _EventCard({required this.event});

  @override
  Widget build(BuildContext context) {
    final dateLabel = DateFormat('EEE, MMM d • h:mm a').format(event.startTime);
    return SizedBox(
      width: 220,
      child: SoftCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(dateLabel, style: const TextStyle(color: AppColors.primary, fontSize: 12, fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            Text(event.title, style: Theme.of(context).textTheme.titleMedium, maxLines: 2, overflow: TextOverflow.ellipsis),
            const Spacer(),
            if (event.location.isNotEmpty)
              Row(
                children: [
                  const Icon(Icons.place_outlined, size: 14, color: AppColors.textMuted),
                  const SizedBox(width: 4),
                  Expanded(child: Text(event.location, style: const TextStyle(fontSize: 12, color: AppColors.textMuted), maxLines: 1, overflow: TextOverflow.ellipsis)),
                ],
              ),
          ],
        ),
      ),
    );
  }
}

class _LeaderAvatar extends StatelessWidget {
  final ClergyModel clergy;
  const _LeaderAvatar({required this.clergy});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 84,
      child: Column(
        children: [
          CircleAvatar(
            radius: 32,
            backgroundColor: AppColors.primarySoft,
            backgroundImage: clergy.photoUrl != null ? NetworkImage(clergy.photoUrl!) : null,
            child: clergy.photoUrl == null ? const Icon(Icons.person, color: AppColors.primary) : null,
          ),
          const SizedBox(height: 6),
          Text(clergy.fullName, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600), maxLines: 1, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center),
          Text(clergy.title, style: const TextStyle(fontSize: 10, color: AppColors.textMuted), maxLines: 1, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center),
        ],
      ),
    );
  }
}
