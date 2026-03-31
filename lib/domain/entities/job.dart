/// Job Intelligent - Job Entity
/// Domain entity representing a job posting.
library;

class JobEntity {
  final int id;
  final String title;
  final String description;
  final String company;
  final String location;
  final String jobType;
  final List<String> skillsRequired;
  final String source;
  final DateTime? createdAt;

  const JobEntity({
    required this.id,
    required this.title,
    required this.description,
    required this.company,
    required this.location,
    required this.jobType,
    required this.skillsRequired,
    required this.source,
    this.createdAt,
  });
}
