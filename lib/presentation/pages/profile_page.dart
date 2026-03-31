/// Job Intelligent - Profile Page
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/theme.dart';
import '../providers/providers.dart';
import '../widgets/skill_chip.dart';

class ProfilePage extends ConsumerStatefulWidget {
  const ProfilePage({super.key});

  @override
  ConsumerState<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends ConsumerState<ProfilePage> {
  bool _editing = false;
  late TextEditingController _nameController;
  late TextEditingController _expController;
  late TextEditingController _skillAddController;
  late List<String> _editSkills;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _expController = TextEditingController();
    _skillAddController = TextEditingController();
    _editSkills = [];
  }

  @override
  void dispose() {
    _nameController.dispose();
    _expController.dispose();
    _skillAddController.dispose();
    super.dispose();
  }

  void _startEditing() {
    final user = ref.read(authProvider).user;
    if (user == null) return;
    _nameController.text = user.fullName;
    _expController.text = user.experience;
    _editSkills = List.from(user.skills);
    setState(() => _editing = true);
  }

  Future<void> _saveProfile() async {
    await ref.read(authProvider.notifier).updateProfile(
          fullName: _nameController.text.trim(),
          skills: _editSkills,
          experience: _expController.text.trim(),
        );
    setState(() => _editing = false);
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
        actions: [
          if (!_editing)
            IconButton(
              icon: const Icon(Icons.edit_outlined),
              onPressed: _startEditing,
            )
          else
            TextButton(
              onPressed: _saveProfile,
              child: const Text('Sauvegarder'),
            ),
        ],
      ),
      body: user == null
          ? const Center(child: Text('Non connecté'))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  // Avatar
                  Container(
                    width: 100,
                    height: 100,
                    decoration: BoxDecoration(
                      gradient: AppColors.primaryGradient,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primary.withValues(alpha: 0.3),
                          blurRadius: 16,
                          offset: const Offset(0, 6),
                        ),
                      ],
                    ),
                    child: Center(
                      child: Text(
                        user.fullName.isNotEmpty ? user.fullName[0].toUpperCase() : '?',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 40,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),

                  if (!_editing) ...[
                    Text(
                      user.fullName,
                      style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      user.email,
                      style: TextStyle(
                        fontSize: 15,
                        color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Skills
                    _SectionCard(
                      title: 'Compétences',
                      icon: Icons.code,
                      child: user.skills.isEmpty
                          ? const Text('Aucune compétence ajoutée')
                          : Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: user.skills
                                  .map((s) => SkillChip(label: s, selected: true))
                                  .toList(),
                            ),
                    ),
                    const SizedBox(height: 12),

                    // Experience
                    _SectionCard(
                      title: 'Expérience',
                      icon: Icons.work_history_outlined,
                      child: Text(
                        user.experience.isEmpty ? 'Aucune expérience renseignée' : user.experience,
                        style: const TextStyle(fontSize: 14, height: 1.5),
                      ),
                    ),
                    const SizedBox(height: 32),

                    // Logout
                    SizedBox(
                      width: double.infinity,
                      height: 48,
                      child: OutlinedButton.icon(
                        onPressed: () async {
                          await ref.read(authProvider.notifier).logout();
                          if (context.mounted) context.go('/login');
                        },
                        icon: const Icon(Icons.logout, color: AppColors.error),
                        label: const Text(
                          'Se déconnecter',
                          style: TextStyle(color: AppColors.error),
                        ),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: AppColors.error),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                      ),
                    ),
                  ] else ...[
                    // Editing mode
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _nameController,
                      decoration: const InputDecoration(
                        labelText: 'Nom complet',
                        prefixIcon: Icon(Icons.person_outline),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _expController,
                      decoration: const InputDecoration(
                        labelText: 'Expérience',
                        prefixIcon: Icon(Icons.work_history_outlined),
                      ),
                      maxLines: 4,
                    ),
                    const SizedBox(height: 16),

                    // Skills edit
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _skillAddController,
                            decoration: const InputDecoration(
                              hintText: 'Ajouter compétence...',
                              prefixIcon: Icon(Icons.code),
                            ),
                            onFieldSubmitted: (v) {
                              if (v.isNotEmpty && !_editSkills.contains(v)) {
                                setState(() {
                                  _editSkills.add(v);
                                  _skillAddController.clear();
                                });
                              }
                            },
                          ),
                        ),
                        IconButton(
                          onPressed: () {
                            final v = _skillAddController.text.trim();
                            if (v.isNotEmpty && !_editSkills.contains(v)) {
                              setState(() {
                                _editSkills.add(v);
                                _skillAddController.clear();
                              });
                            }
                          },
                          icon: const Icon(Icons.add_circle, color: AppColors.primary),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: _editSkills.map((s) {
                        return SkillChip(
                          label: s,
                          selected: true,
                          onDelete: () => setState(() => _editSkills.remove(s)),
                        );
                      }).toList(),
                    ),
                  ],
                ],
              ),
            ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final Widget child;

  const _SectionCard({required this.title, required this.icon, required this.child});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: AppColors.primary, size: 20),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ],
            ),
            const SizedBox(height: 12),
            child,
          ],
        ),
      ),
    );
  }
}
