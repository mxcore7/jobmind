/// Job Intelligent - Home Page
/// Main page with job listings and recommendations.
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/theme.dart';
import '../providers/providers.dart';
import '../widgets/job_card.dart';

class HomePage extends ConsumerStatefulWidget {
  const HomePage({super.key});

  @override
  ConsumerState<HomePage> createState() => _HomePageState();
}

class _HomePageState extends ConsumerState<HomePage> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: IndexedStack(
          index: _currentIndex,
          children: [
            _JobsTab(isDark: isDark, userName: authState.user?.fullName ?? ''),
            _RecommendationsTab(userId: authState.user?.id ?? 0),
          ],
        ),
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          border: Border(
            top: BorderSide(
              color: isDark ? AppColors.borderDark : AppColors.borderLight,
              width: 0.5,
            ),
          ),
        ),
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (i) => setState(() => _currentIndex = i),
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.work_outline),
              activeIcon: Icon(Icons.work),
              label: 'Offres',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.auto_awesome_outlined),
              activeIcon: Icon(Icons.auto_awesome),
              label: 'Pour vous',
            ),
          ],
        ),
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FloatingActionButton.small(
            heroTag: 'search',
            onPressed: () => context.push('/search'),
            backgroundColor: AppColors.accent,
            child: const Icon(Icons.search, color: Colors.white),
          ),
          const SizedBox(height: 8),
          FloatingActionButton.small(
            heroTag: 'fav',
            onPressed: () => context.push('/favorites'),
            backgroundColor: AppColors.error.withValues(alpha: 0.9),
            child: const Icon(Icons.favorite, color: Colors.white),
          ),
          const SizedBox(height: 8),
          FloatingActionButton.small(
            heroTag: 'profile',
            onPressed: () => context.push('/profile'),
            backgroundColor: AppColors.primary,
            child: const Icon(Icons.person, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _JobsTab extends ConsumerWidget {
  final bool isDark;
  final String userName;

  const _JobsTab({required this.isDark, required this.userName});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final jobsAsync = ref.watch(jobsProvider);

    return RefreshIndicator(
      onRefresh: () async {
        ref.invalidate(jobsProvider);
      },
      child: CustomScrollView(
        slivers: [
          // Header
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Bonjour${userName.isNotEmpty ? ', ${userName.split(' ').first}' : ''} 👋',
                    style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Découvrez les dernières offres Data',
                    style: TextStyle(
                      fontSize: 15,
                      color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Search bar shortcut
          SliverToBoxAdapter(
            child: GestureDetector(
              onTap: () => context.push('/search'),
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                decoration: BoxDecoration(
                  color: isDark ? AppColors.surfaceDark : AppColors.surfaceLight,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(
                    color: isDark ? AppColors.borderDark : AppColors.borderLight,
                  ),
                ),
                child: Row(
                  children: [
                    Icon(
                      Icons.search,
                      color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                    ),
                    const SizedBox(width: 12),
                    Text(
                      'Rechercher un poste, une compétence...',
                      style: TextStyle(
                        color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // Section title
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.fromLTRB(20, 8, 20, 4),
              child: Text(
                'Offres récentes',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
              ),
            ),
          ),

          // Jobs list
          jobsAsync.when(
            data: (jobs) {
              if (jobs.isEmpty) {
                return const SliverFillRemaining(
                  child: Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.work_off_outlined, size: 64, color: AppColors.textSecondaryLight),
                        SizedBox(height: 16),
                        Text('Aucune offre disponible', style: TextStyle(fontSize: 16)),
                      ],
                    ),
                  ),
                );
              }
              return SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final job = jobs[index];
                    return JobCard(
                      job: job,
                      onTap: () => context.push('/job/${job.id}'),
                    );
                  },
                  childCount: jobs.length,
                ),
              );
            },
            loading: () => const SliverFillRemaining(
              child: Center(child: CircularProgressIndicator()),
            ),
            error: (err, _) => SliverFillRemaining(
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.cloud_off, size: 48, color: AppColors.error),
                    const SizedBox(height: 12),
                    Text('Erreur: $err', textAlign: TextAlign.center),
                    const SizedBox(height: 12),
                    ElevatedButton(
                      onPressed: () => ref.invalidate(jobsProvider),
                      child: const Text('Réessayer'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _RecommendationsTab extends ConsumerWidget {
  final int userId;

  const _RecommendationsTab({required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    if (userId == 0) {
      return const Center(child: Text('Connectez-vous pour voir vos recommandations'));
    }

    final recoAsync = ref.watch(recommendationsProvider(userId));

    return RefreshIndicator(
      onRefresh: () async {
        ref.invalidate(recommendationsProvider(userId));
      },
      child: CustomScrollView(
        slivers: [
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.fromLTRB(20, 16, 20, 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Recommandations ✨',
                    style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 4),
                  Text(
                    'Jobs personnalisés selon vos compétences',
                    style: TextStyle(fontSize: 15, color: AppColors.textSecondaryLight),
                  ),
                ],
              ),
            ),
          ),
          recoAsync.when(
            data: (recos) {
              if (recos.isEmpty) {
                return const SliverFillRemaining(
                  child: Center(child: Text('Aucune recommandation pour le moment')),
                );
              }
              return SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final reco = recos[index];
                    return JobCard(
                      job: reco.job,
                      score: reco.score,
                      onTap: () => context.push('/job/${reco.job.id}'),
                    );
                  },
                  childCount: recos.length,
                ),
              );
            },
            loading: () => const SliverFillRemaining(
              child: Center(child: CircularProgressIndicator()),
            ),
            error: (err, _) => SliverFillRemaining(
              child: Center(child: Text('Erreur: $err')),
            ),
          ),
        ],
      ),
    );
  }
}
