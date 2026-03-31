/// Job Intelligent - Centralized API Service
/// Dio-based HTTP client with JWT interceptor for all backend communication.
library;

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../core/constants.dart';

class ApiService {
  late final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  ApiService() {
    final baseUrl = kIsWeb
        ? AppConstants.apiBaseUrlWeb
        : (defaultTargetPlatform == TargetPlatform.iOS
            ? AppConstants.apiBaseUrlIos
            : AppConstants.apiBaseUrl);

    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(milliseconds: AppConstants.connectTimeout),
      receiveTimeout: const Duration(milliseconds: AppConstants.receiveTimeout),
      headers: {'Content-Type': 'application/json'},
    ));

    // JWT interceptor
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _storage.read(key: AppConstants.tokenKey);
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) {
        handler.next(error);
      },
    ));
  }

  // --- Token management ---

  Future<void> saveToken(String token) async {
    await _storage.write(key: AppConstants.tokenKey, value: token);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: AppConstants.tokenKey);
  }

  Future<void> clearToken() async {
    await _storage.delete(key: AppConstants.tokenKey);
  }

  // --- Auth ---

  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String fullName,
    List<String> skills = const [],
    String experience = '',
  }) async {
    final response = await _dio.post('/auth/register', data: {
      'email': email,
      'password': password,
      'full_name': fullName,
      'skills': skills,
      'experience': experience,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });
    return response.data;
  }

  // --- Profile ---

  Future<Map<String, dynamic>> getProfile() async {
    final response = await _dio.get('/profile');
    return response.data;
  }

  Future<Map<String, dynamic>> updateProfile(Map<String, dynamic> data) async {
    final response = await _dio.put('/profile', data: data);
    return response.data;
  }

  // --- Jobs ---

  Future<List<dynamic>> getJobs({
    int skip = 0,
    int limit = 50,
    String? location,
    String? jobType,
  }) async {
    final params = <String, dynamic>{
      'skip': skip,
      'limit': limit,
    };
    if (location != null) params['location'] = location;
    if (jobType != null) params['job_type'] = jobType;

    final response = await _dio.get('/jobs', queryParameters: params);
    return response.data;
  }

  Future<Map<String, dynamic>> getJobById(int id) async {
    final response = await _dio.get('/jobs/$id');
    return response.data;
  }

  // --- Recommendations ---

  Future<List<dynamic>> getRecommendations(int userId, {int limit = 20}) async {
    final response = await _dio.get('/recommendations/$userId', queryParameters: {'limit': limit});
    return response.data;
  }

  // --- Search ---

  Future<List<dynamic>> searchJobs({
    String? query,
    String? skills,
    String? location,
    String? jobType,
  }) async {
    final params = <String, dynamic>{};
    if (query != null) params['q'] = query;
    if (skills != null) params['skills'] = skills;
    if (location != null) params['location'] = location;
    if (jobType != null) params['job_type'] = jobType;

    final response = await _dio.get('/search', queryParameters: params);
    return response.data;
  }

  // --- Favorites ---

  Future<List<dynamic>> getFavorites() async {
    final response = await _dio.get('/favorites');
    return response.data;
  }

  Future<void> addFavorite(int jobId) async {
    await _dio.post('/favorites/$jobId');
  }

  Future<void> removeFavorite(int jobId) async {
    await _dio.delete('/favorites/$jobId');
  }

  // --- History ---

  Future<List<dynamic>> getHistory({int limit = 50}) async {
    final response = await _dio.get('/history', queryParameters: {'limit': limit});
    return response.data;
  }
}
