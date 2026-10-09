import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/services/auth_service.dart';
import 'features/auth/screens/splash_screen.dart';

void main() {
  runApp(const MckChurchApp());
}

class MckChurchApp extends StatelessWidget {
  const MckChurchApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<AuthService>.value(
      value: AuthService.instance,
      child: MaterialApp(
        title: 'MCK Wesley Church',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.light,
        home: const SplashScreen(),
      ),
    );
  }
}
