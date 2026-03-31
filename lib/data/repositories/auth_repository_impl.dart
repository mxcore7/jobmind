/// Job Intelligent - Auth Repository Implementation
library;

import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/api_service.dart';
import '../models/user_model.dart';

class AuthRepositoryImpl implements AuthRepository {
  final ApiService _api;

  AuthRepositoryImpl(this._api);

  @override
  Future<({String token, UserEntity user})> register({
    required String email,
    required String password,
    required String fullName,
    List<String> skills = const [],
    String experience = '',
  }) async {
    final data = await _api.register(
      email: email,
      password: password,
      fullName: fullName,
      skills: skills,
      experience: experience,
    );
    final token = data['access_token'] as String;
    final user = UserModel.fromJson(data['user'] as Map<String, dynamic>);
    await _api.saveToken(token);
    return (token: token, user: user);
  }

  @override
  Future<({String token, UserEntity user})> login({
    required String email,
    required String password,
  }) async {
    final data = await _api.login(email: email, password: password);
    final token = data['access_token'] as String;
    final user = UserModel.fromJson(data['user'] as Map<String, dynamic>);
    await _api.saveToken(token);
    return (token: token, user: user);
  }

  @override
  Future<UserEntity> getProfile() async {
    final data = await _api.getProfile();
    return UserModel.fromJson(data);
  }

  @override
  Future<UserEntity> updateProfile({
    String? fullName,
    List<String>? skills,
    String? experience,
    Map<String, dynamic>? preferences,
  }) async {
    final body = <String, dynamic>{};
    if (fullName != null) body['full_name'] = fullName;
    if (skills != null) body['skills'] = skills;
    if (experience != null) body['experience'] = experience;
    if (preferences != null) body['preferences'] = preferences;
    final data = await _api.updateProfile(body);
    return UserModel.fromJson(data);
  }
}
