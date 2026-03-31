/// Job Intelligent - Application Constants
library;

class AppConstants {
  AppConstants._();

  /// API base URL - change to your server address
  static const String apiBaseUrl = 'http://10.0.2.2:8000'; // Android emulator
  static const String apiBaseUrlWeb = 'http://localhost:8000'; // Web
  static const String apiBaseUrlIos = 'http://localhost:8000'; // iOS simulator

  /// API timeouts
  static const int connectTimeout = 15000; // 15s
  static const int receiveTimeout = 15000; // 15s

  /// Storage keys
  static const String tokenKey = 'jwt_token';
  static const String userKey = 'user_data';

  /// App info
  static const String appName = 'Job Intelligent';
  static const String appVersion = '1.0.0';
}
