/// Job Intelligent - Job Data Model
/// JSON serialization/deserialization for Job entities.
library;

import '../../domain/entities/job.dart';

class JobModel extends JobEntity {
  const JobModel({
    required super.id,
    required super.title,
    required super.description,
    required super.company,
    required super.location,
    required super.jobType,
    required super.skillsRequired,
    required super.source,
    super.createdAt,
  });

  factory JobModel.fromJson(Map<String, dynamic> json) {
    return JobModel(
      id: json['id'] as int,
      title: json['title'] as String,
      description: json['description'] as String,
      company: json['company'] as String,
      location: json['location'] as String,
      jobType: json['job_type'] as String? ?? 'CDI',
      skillsRequired: (json['skills_required'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      source: json['source'] as String? ?? 'internal',
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'description': description,
        'company': company,
        'location': location,
        'job_type': jobType,
        'skills_required': skillsRequired,
        'source': source,
      };
}
