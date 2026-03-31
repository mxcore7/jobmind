/// Job Intelligent - Job Repository Interface
library;

import '../entities/job.dart';
import '../entities/recommendation.dart';

abstract class JobRepository {
  Future<List<JobEntity>> getJobs({int skip, int limit, String? location, String? jobType});
  Future<JobEntity> getJobById(int id);
  Future<List<RecommendationEntity>> getRecommendations(int userId, {int limit});
  Future<List<JobEntity>> searchJobs({String? query, String? skills, String? location, String? jobType});

  // Favorites
  Future<List<JobEntity>> getFavorites();
  Future<void> addFavorite(int jobId);
  Future<void> removeFavorite(int jobId);

  // History
  Future<List<JobEntity>> getHistory({int limit});
}
