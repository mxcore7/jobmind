/// Job Intelligent - User Entity
/// Domain entity representing a user.
library;

class UserEntity {
  final int id;
  final String email;
  final String fullName;
  final List<String> skills;
  final String experience;
  final Map<String, dynamic> preferences;
  final DateTime? createdAt;

  const UserEntity({
    required this.id,
    required this.email,
    required this.fullName,
    required this.skills,
    required this.experience,
    required this.preferences,
    this.createdAt,
  });
}
