import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../widgets/state_views.dart';
import '../../../widgets/soft_card.dart';
import '../../../widgets/section_header.dart';
import '../models/donation_model.dart';
import '../models/paybill_model.dart';
import '../services/giving_service.dart';

const Map<String, String> _accountCodes = {
  'T': 'Tithe',
  'O': 'Offering',
  'P': 'Pledge',
  'B': 'Building Fund',
  'E': 'Education',
  'H': 'Harvest',
  'G': 'General',
};

class GivingScreen extends StatefulWidget {
  const GivingScreen({super.key});

  @override
  State<GivingScreen> createState() => _GivingScreenState();
}

class _GivingScreenState extends State<GivingScreen> {
  final _service = GivingService();
  late Future<List<DonationModel>> _historyFuture;
  PaybillModel? _paybill;

  @override
  void initState() {
    super.initState();
    _historyFuture = _service.fetchMyDonations();
    _loadPaybill();
  }

  Future<void> _loadPaybill() async {
    final paybill = await _service.fetchPaybill();
    if (mounted) setState(() => _paybill = paybill);
  }

  Future<void> _refresh() async {
    setState(() => _historyFuture = _service.fetchMyDonations());
    await _historyFuture;
  }

  Future<void> _openRecordGiftSheet() async {
    final formKey = GlobalKey<FormState>();
    String accountCode = 'T';
    final amountController = TextEditingController();
    final refController = TextEditingController();
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
              padding: EdgeInsets.only(
                left: 20, right: 20, top: 20,
                bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
              ),
              child: Form(
                key: formKey,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text('Record a Gift', style: Theme.of(context).textTheme.titleLarge),
                    const SizedBox(height: 4),
                    Text(
                      'After sending money via the paybill above, record it here so it reflects in your giving history.',
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
                    DropdownButtonFormField<String>(
                      value: accountCode,
                      decoration: const InputDecoration(labelText: 'Account'),
                      items: _accountCodes.entries
                          .map((e) => DropdownMenuItem(value: e.key, child: Text(e.value)))
                          .toList(),
                      onChanged: (v) => setSheetState(() => accountCode = v!),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: amountController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(labelText: 'Amount (KES)'),
                      validator: (v) => (v == null || double.tryParse(v) == null) ? 'Enter a valid amount' : null,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: refController,
                      decoration: const InputDecoration(labelText: 'M-Pesa Reference (optional)'),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: submitting
                          ? null
                          : () async {
                              if (!formKey.currentState!.validate()) return;
                              setSheetState(() {
                                submitting = true;
                                error = null;
                              });
                              try {
                                await _service.recordDonation(
                                  accountCode: accountCode,
                                  amount: double.parse(amountController.text),
                                  mpesaRef: refController.text.trim().isEmpty ? null : refController.text.trim(),
                                );
                                if (context.mounted) Navigator.pop(ctx);
                                _refresh();
                              } catch (_) {
                                setSheetState(() {
                                  submitting = false;
                                  error = 'Could not save this record. Please try again.';
                                });
                              }
                            },
                      child: submitting
                          ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                          : const Text('Save Record'),
                    ),
                  ],
                ),
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
      appBar: AppBar(title: const Text('Give')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: AppColors.primary,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            _buildPaybillCard(),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: _openRecordGiftSheet,
              icon: const Icon(Icons.add),
              label: const Text('Record a Gift'),
            ),
            const SizedBox(height: 24),
            const SectionHeader(title: 'My Giving History'),
            const SizedBox(height: 12),
            FutureBuilder<List<DonationModel>>(
              future: _historyFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Padding(padding: EdgeInsets.symmetric(vertical: 40), child: LoadingView());
                }
                if (snapshot.hasError) {
                  return ErrorView(message: 'Could not load your giving history.', onRetry: _refresh);
                }
                final donations = snapshot.data!;
                if (donations.isEmpty) {
                  return const SoftCard(child: EmptyView(message: 'No giving history yet.', icon: Icons.receipt_long_outlined));
                }
                return Column(
                  children: donations.map((d) => Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: SoftCard(
                      child: Row(
                        children: [
                          Container(
                            width: 40, height: 40,
                            alignment: Alignment.center,
                            decoration: BoxDecoration(color: AppColors.successSoft, borderRadius: BorderRadius.circular(AppRadius.sm)),
                            child: const Icon(Icons.arrow_upward, color: AppColors.success, size: 18),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(d.accountCodeDisplay, style: Theme.of(context).textTheme.titleMedium),
                                Text(DateFormat('d MMM yyyy').format(d.createdAt), style: Theme.of(context).textTheme.bodyMedium),
                              ],
                            ),
                          ),
                          Text(
                            'KES ${NumberFormat('#,##0').format(d.amount)}',
                            style: const TextStyle(fontWeight: FontWeight.w800, color: AppColors.success),
                          ),
                        ],
                      ),
                    ),
                  )).toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPaybillCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryLight], begin: Alignment.topLeft, end: Alignment.bottomRight),
        borderRadius: BorderRadius.circular(AppRadius.lg),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Church Paybill Number', style: TextStyle(color: Colors.white70, fontSize: 13)),
          const SizedBox(height: 6),
          Text(
            _paybill?.number ?? '—',
            style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.w800, letterSpacing: 1),
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: _accountCodes.values.map((label) => Chip(
              label: Text(label),
              backgroundColor: Colors.white24,
              labelStyle: const TextStyle(color: Colors.white, fontSize: 11),
            )).toList(),
          ),
        ],
      ),
    );
  }
}
