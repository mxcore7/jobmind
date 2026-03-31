/// Job Intelligent - Auth Repository Interface
library;

import '../entities/user.dart';

abstract class AuthRepository {
  Future<({String token, UserEntity user})> register({
    required String email,
    required String password,
    required String fullName,
    List<String> skills,
    String experience,
  });

  Future<({String token, UserEntity user})> login({
    required String email,
    required String password,
  });

  Future<UserEntity> getProfile();
  Future<UserEntity> updateProfile({
    String? fullName,
    List<String>? skills,
    String? experience,
    Map<String, dynamic>? preferences,
  });
}
