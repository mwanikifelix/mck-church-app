import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../models/membership_card_model.dart';
import '../services/profile_service.dart';

class MembershipCardScreen extends StatefulWidget {
  const MembershipCardScreen({super.key});

  @override
  State<MembershipCardScreen> createState() => _MembershipCardScreenState();
}

class _MembershipCardScreenState extends State<MembershipCardScreen> {
  final _service = ProfileService();
  late Future<MembershipCardModel> _cardFuture;
  Uint8List? _qrBytes;
  bool _loadingQr = false;

  @override
  void initState() {
    super.initState();
    _cardFuture = _service.fetchMyCard();
  }

  Future<void> _loadQr() async {
    setState(() => _loadingQr = true);
    try {
      final bytes = await _service.fetchMyQrCode();
      setState(() {
        _qrBytes = bytes;
        _loadingQr = false;
      });
    } catch (_) {
      setState(() => _loadingQr = false);
    }
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'active':
        return AppColors.success;
      case 'inactive':
        return AppColors.warning;
      default:
        return AppColors.textMuted;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Membership Card')),
      body: FutureBuilder<MembershipCardModel>(
        future: _cardFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return const LoadingView();
          if (snapshot.hasError) {
            return ErrorView(message: 'Could not load your card.', onRetry: () => setState(() => _cardFuture = _service.fetchMyCard()));
          }
          final card = snapshot.data!;
          return SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                _buildCardFront(card),
                const SizedBox(height: 20),
                if (_qrBytes == null)
                  OutlinedButton.icon(
                    onPressed: _loadingQr ? null : _loadQr,
                    icon: _loadingQr
                        ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                        : const Icon(Icons.qr_code_2),
                    label: Text(_loadingQr ? 'Loading...' : 'Show QR Code'),
                  )
                else
                  SoftCardQr(bytes: _qrBytes!),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildCardFront(MembershipCardModel card) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryLight], begin: Alignment.topLeft, end: Alignment.bottomRight),
        borderRadius: BorderRadius.circular(AppRadius.lg),
        boxShadow: [BoxShadow(color: AppColors.primary.withValues(alpha: 0.3), blurRadius: 20, offset: const Offset(0, 8))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.church, color: Colors.white, size: 20),
              SizedBox(width: 8),
              Text('MCK WESLEY CHURCH', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13, letterSpacing: 0.5)),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CircleAvatar(
                radius: 36,
                backgroundColor: Colors.white24,
                backgroundImage: card.passportPhoto != null ? NetworkImage(card.passportPhoto!) : null,
                child: card.passportPhoto == null ? const Icon(Icons.person, color: Colors.white, size: 36) : null,
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(card.fullName, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 18)),
                    const SizedBox(height: 4),
                    Text(card.membershipNumber, style: const TextStyle(color: Colors.white70, fontSize: 13, letterSpacing: 1)),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                      decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(AppRadius.pill)),
                      child: Text(
                        card.status.toUpperCase(),
                        style: TextStyle(color: _statusColor(card.status) == AppColors.success ? Colors.white : Colors.white, fontSize: 10, fontWeight: FontWeight.w800),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          const Divider(color: Colors.white24),
          const SizedBox(height: 12),
          _cardInfoRow('Branch', card.branchName ?? 'Not assigned'),
          _cardInfoRow('Category', card.growthTrackCategory ?? '-'),
          _cardInfoRow('HBC Group', card.hbcGroupName ?? 'Not assigned'),
          _cardInfoRow('Departments', card.departmentNames.isEmpty ? 'None' : card.departmentNames.join(', ')),
          _cardInfoRow('Issued', DateFormat('d MMM yyyy').format(card.dateIssued)),
        ],
      ),
    );
  }

  Widget _cardInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 100, child: Text(label, style: const TextStyle(color: Colors.white60, fontSize: 12))),
          Expanded(child: Text(value, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600))),
        ],
      ),
    );
  }
}

class SoftCardQr extends StatelessWidget {
  final Uint8List bytes;
  const SoftCardQr({super.key, required this.bytes});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.border),
      ),
      child: Image.memory(bytes, width: 200, height: 200),
    );
  }
}
