/// Job Intelligent - Application Entry Point
/// Flutter app with Riverpod, GoRouter, and Material 3 theming.
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/date_symbol_data_local.dart';

import 'core/theme.dart';
import 'core/router.dart';
import 'presentation/providers/providers.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('fr');
  
  // Read auth token before building the UI to avoid redirecting to login on web refresh
  final container = ProviderContainer();
  await container.read(authProvider.notifier).checkAuth();

  runApp(UncontrolledProviderScope(
    container: container,
    child: const JobIntelligentApp(),
  ));
}

class JobIntelligentApp extends ConsumerWidget {
  const JobIntelligentApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'Job Intelligent',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routerConfig: router,
    );
  }
}
