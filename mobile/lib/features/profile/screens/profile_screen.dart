import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/soft_card.dart';
import '../../auth/services/auth_service.dart';
import '../../auth/screens/login_screen.dart';
import 'membership_card_screen.dart';
import '../../groups/screens/groups_screen.dart';
import '../../prayer/screens/prayer_screen.dart';
import '../../counselling/screens/counselling_screen.dart';
import '../../catechism/screens/catechism_screen.dart';
import '../../attendance/screens/attendance_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  Future<void> _confirmLogout(BuildContext context) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Log Out'),
        content: const Text('Are you sure you want to log out?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
          TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Log Out', style: TextStyle(color: AppColors.danger))),
        ],
      ),
    );
    if (confirmed == true && context.mounted) {
      await AuthService.instance.logout();
      if (context.mounted) {
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const LoginScreen()),
          (route) => false,
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthService>().currentUser;

    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            SoftCard(
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 32,
                    backgroundColor: AppColors.primarySoft,
                    backgroundImage: user?.passportPhoto != null ? NetworkImage(user!.passportPhoto!) : null,
                    child: user?.passportPhoto == null ? const Icon(Icons.person, color: AppColors.primary, size: 28) : null,
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(user?.fullName ?? '', style: Theme.of(context).textTheme.titleMedium),
                        const SizedBox(height: 2),
                        Text(user?.email ?? '', style: Theme.of(context).textTheme.bodyMedium),
                        const SizedBox(height: 4),
                        Text(user?.membershipNumber ?? '', style: const TextStyle(color: AppColors.primary, fontSize: 12, fontWeight: FontWeight.w700)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            _ProfileMenuItem(
              icon: Icons.badge_outlined,
              label: 'My Membership Card',
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const MembershipCardScreen())),
            ),
            _ProfileMenuItem(icon: Icons.person_outline, label: 'Edit Profile', onTap: () {}),
            _ProfileMenuItem(icon: Icons.notifications_outlined, label: 'Notifications', onTap: () {}),
            _ProfileMenuItem(
              icon: Icons.groups_outlined,
              label: 'Groups & Departments',
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const GroupsScreen())),
            ),
            _ProfileMenuItem(
              icon: Icons.location_on_outlined,
              label: 'Sunday Attendance',
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const AttendanceScreen())),
            ),
            _ProfileMenuItem(
              icon: Icons.favorite_border,
              label: 'Prayer Requests',
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const PrayerScreen())),
            ),
            _ProfileMenuItem(
              icon: Icons.support_agent_outlined,
              label: 'Counselling',
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const CounsellingScreen())),
            ),
            _ProfileMenuItem(
              icon: Icons.school_outlined,
              label: 'Catechism Registration',
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const CatechismScreen())),
            ),
            _ProfileMenuItem(icon: Icons.help_outline, label: 'Help & Support', onTap: () {}),
            const SizedBox(height: 12),
            _ProfileMenuItem(
              icon: Icons.logout,
              label: 'Log Out',
              iconColor: AppColors.danger,
              labelColor: AppColors.danger,
              onTap: () => _confirmLogout(context),
            ),
          ],
        ),
      ),
    );
  }
}

class _ProfileMenuItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;
  final Color? iconColor;
  final Color? labelColor;

  const _ProfileMenuItem({
    required this.icon,
    required this.label,
    required this.onTap,
    this.iconColor,
    this.labelColor,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: SoftCard(
        onTap: onTap,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        child: Row(
          children: [
            Icon(icon, color: iconColor ?? AppColors.textSecondary, size: 22),
            const SizedBox(width: 14),
            Expanded(child: Text(label, style: TextStyle(fontWeight: FontWeight.w600, color: labelColor ?? AppColors.textPrimary))),
            const Icon(Icons.chevron_right, color: AppColors.textMuted),
          ],
        ),
      ),
    );
  }
}
