/// Job Intelligent - Recommendation Entity
library;

import 'job.dart';

class RecommendationEntity {
  final JobEntity job;
  final double score;
  final String matchType;

  const RecommendationEntity({
    required this.job,
    required this.score,
    required this.matchType,
  });
}
