/// Job Intelligent - Job Repository Implementation
library;

import '../../domain/entities/job.dart';
import '../../domain/entities/recommendation.dart';
import '../../domain/repositories/job_repository.dart';
import '../datasources/api_service.dart';
import '../models/job_model.dart';

class JobRepositoryImpl implements JobRepository {
  final ApiService _api;

  JobRepositoryImpl(this._api);

  @override
  Future<List<JobEntity>> getJobs({
    int skip = 0,
    int limit = 50,
    String? location,
    String? jobType,
  }) async {
    final data = await _api.getJobs(
      skip: skip,
      limit: limit,
      location: location,
      jobType: jobType,
    );
    return data.map((j) => JobModel.fromJson(j as Map<String, dynamic>)).toList();
  }

  @override
  Future<JobEntity> getJobById(int id) async {
    final data = await _api.getJobById(id);
    return JobModel.fromJson(data);
  }

  @override
  Future<List<RecommendationEntity>> getRecommendations(int userId, {int limit = 20}) async {
    final data = await _api.getRecommendations(userId, limit: limit);
    return data.map((r) {
      final map = r as Map<String, dynamic>;
      return RecommendationEntity(
        job: JobModel.fromJson(map['job'] as Map<String, dynamic>),
        score: (map['score'] as num).toDouble(),
        matchType: map['match_type'] as String,
      );
    }).toList();
  }

  @override
  Future<List<JobEntity>> searchJobs({
    String? query,
    String? skills,
    String? location,
    String? jobType,
  }) async {
    final data = await _api.searchJobs(
      query: query,
      skills: skills,
      location: location,
      jobType: jobType,
    );
    return data.map((j) => JobModel.fromJson(j as Map<String, dynamic>)).toList();
  }

  @override
  Future<List<JobEntity>> getFavorites() async {
    final data = await _api.getFavorites();
    return data.map((j) => JobModel.fromJson(j as Map<String, dynamic>)).toList();
  }

  @override
  Future<void> addFavorite(int jobId) async {
    await _api.addFavorite(jobId);
  }

  @override
  Future<void> removeFavorite(int jobId) async {
    await _api.removeFavorite(jobId);
  }

  @override
  Future<List<JobEntity>> getHistory({int limit = 50}) async {
    final data = await _api.getHistory(limit: limit);
    return data.map((j) => JobModel.fromJson(j as Map<String, dynamic>)).toList();
  }
}
