/// Job Intelligent - Riverpod Providers
/// Central provider definitions for dependency injection and state management.
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/datasources/api_service.dart';
import '../../data/repositories/auth_repository_impl.dart';
import '../../data/repositories/job_repository_impl.dart';
import '../../domain/entities/job.dart';
import '../../domain/entities/recommendation.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/repositories/job_repository.dart';

// ======================== Core Providers ========================

final apiServiceProvider = Provider<ApiService>((ref) => ApiService());

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepositoryImpl(ref.watch(apiServiceProvider));
});

final jobRepositoryProvider = Provider<JobRepository>((ref) {
  return JobRepositoryImpl(ref.watch(apiServiceProvider));
});

// ======================== Auth State ========================

class AuthState {
  final UserEntity? user;
  final bool isLoading;
  final String? error;
  final bool isAuthenticated;

  const AuthState({
    this.user,
    this.isLoading = false,
    this.error,
    this.isAuthenticated = false,
  });

  AuthState copyWith({
    UserEntity? user,
    bool? isLoading,
    String? error,
    bool? isAuthenticated,
  }) {
    return AuthState(
      user: user ?? this.user,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _authRepo;
  final ApiService _apiService;

  AuthNotifier(this._authRepo, this._apiService) : super(const AuthState());

  Future<bool> register({
    required String email,
    required String password,
    required String fullName,
    List<String> skills = const [],
    String experience = '',
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final result = await _authRepo.register(
        email: email,
        password: password,
        fullName: fullName,
        skills: skills,
        experience: experience,
      );
      state = state.copyWith(
        user: result.user,
        isLoading: false,
        isAuthenticated: true,
      );
      return true;
    } catch (e) {
      state = state.copyWith(isLoading: false, error: _extractError(e));
      return false;
    }
  }

  Future<bool> login({required String email, required String password}) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final result = await _authRepo.login(email: email, password: password);
      state = state.copyWith(
        user: result.user,
        isLoading: false,
        isAuthenticated: true,
      );
      return true;
    } catch (e) {
      state = state.copyWith(isLoading: false, error: _extractError(e));
      return false;
    }
  }

  Future<void> loadProfile() async {
    try {
      final user = await _authRepo.getProfile();
      state = state.copyWith(user: user, isAuthenticated: true);
    } catch (_) {
      // Not authenticated
    }
  }

  Future<void> updateProfile({
    String? fullName,
    List<String>? skills,
    String? experience,
  }) async {
    state = state.copyWith(isLoading: true);
    try {
      final user = await _authRepo.updateProfile(
        fullName: fullName,
        skills: skills,
        experience: experience,
      );
      state = state.copyWith(user: user, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: _extractError(e));
    }
  }

  Future<void> logout() async {
    await _apiService.clearToken();
    state = const AuthState();
  }

  Future<void> checkAuth() async {
    final token = await _apiService.getToken();
    if (token != null) {
      await loadProfile();
    }
  }

  String _extractError(dynamic e) {
    if (e is Exception) {
      final msg = e.toString();
      // Try to extract DioException message
      if (msg.contains('detail')) {
        final start = msg.indexOf('"detail"');
        if (start != -1) {
          final sub = msg.substring(start);
          final colonIdx = sub.indexOf(':');
          final endIdx = sub.indexOf('}');
          if (colonIdx != -1 && endIdx != -1) {
            return sub.substring(colonIdx + 1, endIdx).replaceAll('"', '').trim();
          }
        }
      }
      return 'Une erreur est survenue';
    }
    return 'Erreur inconnue';
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(
    ref.watch(authRepositoryProvider),
    ref.watch(apiServiceProvider),
  );
});

// ======================== Job Providers ========================

final jobsProvider = FutureProvider<List<JobEntity>>((ref) async {
  final repo = ref.watch(jobRepositoryProvider);
  return repo.getJobs();
});

final jobDetailProvider = FutureProvider.family<JobEntity, int>((ref, id) async {
  final repo = ref.watch(jobRepositoryProvider);
  return repo.getJobById(id);
});

final recommendationsProvider = FutureProvider.family<List<RecommendationEntity>, int>((ref, userId) async {
  final repo = ref.watch(jobRepositoryProvider);
  return repo.getRecommendations(userId);
});

final favoritesProvider = FutureProvider<List<JobEntity>>((ref) async {
  final repo = ref.watch(jobRepositoryProvider);
  return repo.getFavorites();
});

final historyProvider = FutureProvider<List<JobEntity>>((ref) async {
  final repo = ref.watch(jobRepositoryProvider);
  return repo.getHistory();
});

// ======================== Search State ========================

class SearchState {
  final List<JobEntity> results;
  final bool isLoading;
  final String? error;
  final String query;
  final String? skills;
  final String? location;
  final String? jobType;

  const SearchState({
    this.results = const [],
    this.isLoading = false,
    this.error,
    this.query = '',
    this.skills,
    this.location,
    this.jobType,
  });

  SearchState copyWith({
    List<JobEntity>? results,
    bool? isLoading,
    String? error,
    String? query,
    String? skills,
    String? location,
    String? jobType,
  }) {
    return SearchState(
      results: results ?? this.results,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      query: query ?? this.query,
      skills: skills ?? this.skills,
      location: location ?? this.location,
      jobType: jobType ?? this.jobType,
    );
  }
}

class SearchNotifier extends StateNotifier<SearchState> {
  final JobRepository _jobRepo;

  SearchNotifier(this._jobRepo) : super(const SearchState());

  Future<void> search({
    String? query,
    String? skills,
    String? location,
    String? jobType,
  }) async {
    state = state.copyWith(
      isLoading: true,
      error: null,
      query: query ?? state.query,
      skills: skills,
      location: location,
      jobType: jobType,
    );
    try {
      final results = await _jobRepo.searchJobs(
        query: query,
        skills: skills,
        location: location,
        jobType: jobType,
      );
      state = state.copyWith(results: results, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  void clearSearch() {
    state = const SearchState();
  }
}

final searchProvider = StateNotifierProvider<SearchNotifier, SearchState>((ref) {
  return SearchNotifier(ref.watch(jobRepositoryProvider));
});
