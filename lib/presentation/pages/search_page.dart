/// Job Intelligent - Search Page
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/theme.dart';
import '../providers/providers.dart';
import '../widgets/job_card.dart';

class SearchPage extends ConsumerStatefulWidget {
  const SearchPage({super.key});

  @override
  ConsumerState<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends ConsumerState<SearchPage> {
  final _queryController = TextEditingController();
  final _skillsController = TextEditingController();
  String? _selectedLocation;
  String? _selectedJobType;
  bool _showFilters = false;

  static const _locations = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Nantes', 'Lille'];
  static const _jobTypes = ['CDI', 'CDD', 'Stage', 'Freelance'];

  @override
  void dispose() {
    _queryController.dispose();
    _skillsController.dispose();
    super.dispose();
  }

  void _search() {
    ref.read(searchProvider.notifier).search(
          query: _queryController.text.isNotEmpty ? _queryController.text : null,
          skills: _skillsController.text.isNotEmpty ? _skillsController.text : null,
          location: _selectedLocation,
          jobType: _selectedJobType,
        );
  }

  @override
  Widget build(BuildContext context) {
    final searchState = ref.watch(searchProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Rechercher'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
        actions: [
          IconButton(
            icon: Icon(_showFilters ? Icons.filter_list_off : Icons.filter_list),
            onPressed: () => setState(() => _showFilters = !_showFilters),
          ),
        ],
      ),
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _queryController,
                    decoration: InputDecoration(
                      hintText: 'Data Scientist, Python, ML...',
                      prefixIcon: const Icon(Icons.search),
                      suffixIcon: _queryController.text.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear, size: 18),
                              onPressed: () {
                                _queryController.clear();
                                setState(() {});
                              },
                            )
                          : null,
                    ),
                    onChanged: (_) => setState(() {}),
                    onFieldSubmitted: (_) => _search(),
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  decoration: BoxDecoration(
                    gradient: AppColors.primaryGradient,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: IconButton(
                    onPressed: _search,
                    icon: const Icon(Icons.search, color: Colors.white),
                  ),
                ),
              ],
            ),
          ),

          // Filters
          if (_showFilters)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: isDark ? AppColors.surfaceDark : AppColors.surfaceLight,
                border: Border(
                  bottom: BorderSide(
                    color: isDark ? AppColors.borderDark : AppColors.borderLight,
                  ),
                ),
              ),
              child: Column(
                children: [
                  // Skills
                  TextFormField(
                    controller: _skillsController,
                    decoration: const InputDecoration(
                      hintText: 'Compétences (Python, SQL, ...)',
                      prefixIcon: Icon(Icons.code),
                      isDense: true,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      // Location dropdown
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          isExpanded: true,
                          decoration: const InputDecoration(
                            hintText: 'Localisation',
                            prefixIcon: Icon(Icons.location_on_outlined),
                            isDense: true,
                          ),
                          initialValue: _selectedLocation,
                          items: [
                            const DropdownMenuItem(value: null, child: Text('Toutes')),
                            ..._locations.map((l) => DropdownMenuItem(value: l, child: Text(l))),
                          ],
                          onChanged: (v) => setState(() => _selectedLocation = v),
                        ),
                      ),
                      const SizedBox(width: 10),
                      // Job type dropdown
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          isExpanded: true,
                          decoration: const InputDecoration(
                            hintText: 'Type',
                            prefixIcon: Icon(Icons.work_outline),
                            isDense: true,
                          ),
                          initialValue: _selectedJobType,
                          items: [
                            const DropdownMenuItem(value: null, child: Text('Tous')),
                            ..._jobTypes.map((t) => DropdownMenuItem(value: t, child: Text(t))),
                          ],
                          onChanged: (v) => setState(() => _selectedJobType = v),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                ],
              ),
            ),

          // Results
          Expanded(
            child: searchState.isLoading
                ? const Center(child: CircularProgressIndicator())
                : searchState.results.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              Icons.manage_search,
                              size: 64,
                              color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                            ),
                            const SizedBox(height: 16),
                            Text(
                              searchState.query.isEmpty
                                  ? 'Commencez votre recherche'
                                  : 'Aucun résultat trouvé',
                              style: TextStyle(
                                fontSize: 16,
                                color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                              ),
                            ),
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.only(top: 8),
                        itemCount: searchState.results.length,
                        itemBuilder: (context, index) {
                          final job = searchState.results[index];
                          return JobCard(
                            job: job,
                            onTap: () => context.push('/job/${job.id}'),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}
